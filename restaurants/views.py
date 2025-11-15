from django.shortcuts import render
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Restaurant, Cuisine, RestaurantCuisine, MenuItem


def restaurant_list(request):
    restaurants = Restaurant.objects.filter(is_active=True).select_related('owner').prefetch_related('hours')
    
    # Filter by cuisine if provided
    cuisine_id = request.GET.get('cuisine')
    if cuisine_id:
        restaurants = restaurants.filter(restaurantcuisine__cuisine_id=cuisine_id)
    
    # Search by name or menu items if provided
    search_query = request.GET.get('search')
    if search_query:
        # Search in restaurant names, descriptions, and menu item names/descriptions
        restaurants = restaurants.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(menu_items__name__icontains=search_query) |
            Q(menu_items__description__icontains=search_query)
        ).distinct()
    
    # Order by rating
    restaurants = restaurants.order_by('-rating')
    
    # Pagination
    paginator = Paginator(restaurants, 10)  # Show 10 restaurants per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Get all cuisines for filter dropdown
    cuisines = Cuisine.objects.all()
    
    context = {
        'page_obj': page_obj,
        'cuisines': cuisines,
        'selected_cuisine': int(cuisine_id) if cuisine_id else None,
        'search_query': search_query,
    }
    return render(request, 'restaurants/restaurant_list.html', context)


def restaurant_detail(request, restaurant_id):
    restaurant = Restaurant.objects.select_related('owner').prefetch_related(
        'hours', 'menu_items', 'reviews'
    ).get(id=restaurant_id)
    
    context = {
        'restaurant': restaurant,
    }
    return render(request, 'restaurants/restaurant_detail.html', context)