from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Review
from .forms import ReviewForm
from django.core.paginator import Paginator

def review_list(request):
    reviews = Review.objects.filter(is_published=True).order_by('-created_at')
    
    # Пагинация
    paginator = Paginator(reviews, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'reviews/review_list.html', {
        'page_obj': page_obj,
    })

@login_required
def add_review(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.save()
            messages.success(request, 'Ваш отзыв отправлен на модерацию. Спасибо!')
            return redirect('reviews:list')
    else:
        # Проверяем, оставлял ли пользователь уже отзыв
        if Review.objects.filter(user=request.user).exists():
            messages.warning(request, 'Вы уже оставляли отзыв.')
            return redirect('reviews:list')
        form = ReviewForm()
    
    return render(request, 'reviews/add_review.html', {'form': form})
