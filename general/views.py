from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import logout
from datetime import datetime, timedelta
import json  
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from general.models import Yacht, Booking, UserProfile
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_protect

def index(request):
    # Получаем все яхты и сортируем их по цене (можно изменить критерий сортировки)
    featured_yachts = Yacht.objects.all().order_by('-price_per_day')[:6]  # Показываем 6 яхт
    yachts = Yacht.objects.all()
    locations = Yacht.objects.values_list('location', flat=True).distinct()
    
    return render(request, 'index.html', {
        'featured_yachts': featured_yachts,  # Добавляем featured_yachts в контекст
        'yachts': yachts,
        'locations': locations,
        'search_query': '',
        'yacht_type': '',
        'selected_location': ''
    })

def about(request):
    return render(request, 'about.html')

def logout_view(request):
    logout(request)
    return redirect('login')

def yacht_page(request):
    yachts = Yacht.objects.all()
    
    # Получаем параметры поиска
    search_query = request.GET.get('search', '')
    location = request.GET.get('location', '')

    # Применяем фильтры
    if search_query:
        yachts = yachts.filter(name__icontains=search_query)
    if location:
        yachts = yachts.filter(location=location)

    # Получаем список уникальных локаций
    locations = Yacht.objects.values_list('location', flat=True).distinct()
    
    return render(request, 'yacht-page.html', {
        'yachts': yachts,
        'locations': locations,
        'search_query': search_query,
        'selected_location': location
    })

def yacht_detail(request, pk):
    yacht = get_object_or_404(Yacht, pk=pk)
    bookings = Booking.objects.filter(yacht=yacht)

    booked_dates = []
    for booking in bookings:
        current_date = booking.start_date
        while current_date <= booking.end_date:
            booked_dates.append(current_date.strftime('%Y-%m-%d'))
            current_date += timedelta(days=1)

    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('login')
        
        start_date_str = request.POST.get('start_date')
        end_date_str = request.POST.get('end_date')
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()

        # Проверка на занятость
        for booking in bookings:
            current_date = booking.start_date
            while current_date <= booking.end_date:
                if start_date <= current_date <= end_date:
                    return render(request, 'yacht_detail.html', {
                        'yacht': yacht,
                        'booked_dates_json': json.dumps(booked_dates),
                        'error': 'Выбранные даты уже заняты.'
                    })
                current_date += timedelta(days=1)

        Booking.objects.create(
            yacht=yacht,
            user=request.user,
            start_date=start_date,
            end_date=end_date,
            is_cancelled=False
        )
        return redirect('yacht_detail', pk=pk)

    return render(request, 'yacht_detail.html', {
        'yacht': yacht,
        'booked_dates_json': json.dumps(booked_dates)
    })

@login_required
def book_yacht(request, yacht_id):
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Метод не поддерживается'})

    yacht = get_object_or_404(Yacht, id=yacht_id)
    start_date = request.POST.get('start_date')
    end_date = request.POST.get('end_date')

    if not start_date or not end_date:
        return JsonResponse({'success': False, 'error': 'Необходимо указать даты бронирования'})

    try:
        start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
    except ValueError:
        return JsonResponse({'success': False, 'error': 'Неверный формат дат'})

    # Проверяем, не занята ли яхта на эти даты
    conflicting_bookings = Booking.objects.filter(
        yacht=yacht,
        start_date__lte=end_date,
        end_date__gte=start_date
    )

    if conflicting_bookings.exists():
        return JsonResponse({'success': False, 'error': 'Яхта уже забронирована на эти даты'})

    # Создаем бронирование
    try:
        Booking.objects.create(
            yacht=yacht,
            user=request.user,
            start_date=start_date,
            end_date=end_date,
            is_cancelled=False
        )
        return JsonResponse({
            'success': True,
            'message': 'Бронирование успешно создано',
            'redirect_url': '/my-bookings/'  # URL для перенаправления после успешного бронирования
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

@login_required
def profile(request):
    user_bookings = Booking.objects.filter(user=request.user).order_by('-start_date')
    upcoming_bookings = user_bookings.filter(start_date__gte=datetime.now().date())
    past_bookings = user_bookings.filter(start_date__lt=datetime.now().date())
    
    if request.method == 'POST':
        # Обновление профиля
        user = request.user
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        user.email = request.POST.get('email', user.email)
        user.save()

        profile = user.profile
        profile.phone = request.POST.get('phone', profile.phone)
        profile.address = request.POST.get('address', profile.address)
        profile.bio = request.POST.get('bio', profile.bio)

        if 'avatar' in request.FILES:
            profile.avatar = request.FILES['avatar']
        
        profile.save()
        messages.success(request, 'Профиль успешно обновлен!')
        return redirect('profile')

    return render(request, 'profile.html', {
        'upcoming_bookings': upcoming_bookings,
        'past_bookings': past_bookings
    })

@login_required
def my_bookings(request):
    user_bookings = Booking.objects.filter(user=request.user).order_by('-start_date')
    upcoming_bookings = user_bookings.filter(start_date__gte=datetime.now().date())
    past_bookings = user_bookings.filter(start_date__lt=datetime.now().date())
    
    if request.method == 'POST':
        # Обновление профиля
        user = request.user
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        user.email = request.POST.get('email', user.email)
        user.save()

        profile = user.profile
        profile.phone = request.POST.get('phone', profile.phone)
        profile.address = request.POST.get('address', profile.address)
        profile.bio = request.POST.get('bio', profile.bio)

        if 'avatar' in request.FILES:
            profile.avatar = request.FILES['avatar']
        
        profile.save()
        messages.success(request, 'Профиль успешно обновлен!')
        return redirect('my_bookings')

    return render(request, 'my_bookings.html', {
        'upcoming_bookings': upcoming_bookings,
        'past_bookings': past_bookings
    })

@csrf_protect
def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')

        # Проверка валидности данных
        if not all([username, email, password1, password2, first_name, last_name]):
            return JsonResponse({
                'success': False,
                'errors': 'Все поля обязательны для заполнения'
            })

        if password1 != password2:
            return JsonResponse({
                'success': False,
                'errors': 'Пароли не совпадают'
            })

        if User.objects.filter(username=username).exists():
            return JsonResponse({
                'success': False,
                'errors': 'Пользователь с таким именем уже существует'
            })

        if User.objects.filter(email=email).exists():
            return JsonResponse({
                'success': False,
                'errors': 'Пользователь с таким email уже существует'
            })

        try:
            # Создаем нового пользователя
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password1
            )
            user.first_name = first_name
            user.last_name = last_name
            user.save()
            return JsonResponse({
                'success': True,
                'message': 'Регистрация успешна'
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'errors': str(e)
            })

    return JsonResponse({
        'success': False,
        'errors': 'Метод не поддерживается'
    })
    
   