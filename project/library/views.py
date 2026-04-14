from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Book, Wishlist
from datetime import timedelta
from django.utils import timezone

#REGISTER
def register(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect('register')
        User.objects.create_user(username=username, password=password)
        messages.success(request, "Registration successful")
        return redirect('login')
    return render(request, 'register.html')


#LOGIN
def user_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, "Login successful ✅")
            return redirect('all_books')
        else:
            messages.error(request, "Invalid username or password ❌")
    return render(request, 'login.html')


# LOGOUT
def user_logout(request):
    logout(request)
    return redirect('login')


# HOME (ADMIN ADD + EDIT BOOKS)
@login_required(login_url='login')
def home(request):
    books = Book.objects.all()
    edit_book = None
    if request.method == "POST":
        book_id = request.POST.get('book_id')

        # UPDATE
        if book_id:
            book = Book.objects.get(id=book_id)
            book.title = request.POST.get('title')
            book.author = request.POST.get('author')
            book.price = request.POST.get('price')

            if request.FILES.get('image'):
                book.image = request.FILES.get('image')

            book.save()

        # ADD
        else:
            title = request.POST.get('title')
            author = request.POST.get('author')
            price = request.POST.get('price')
            image = request.FILES.get('image')

            if title and author and image:
                Book.objects.create(
                    title=title,
                    author=author,
                    price=price,
                    image=image
                )

        return redirect('home')

    # EDIT MODE
    edit_id = request.GET.get('edit')
    if edit_id:
        edit_book = Book.objects.get(id=edit_id)

    return render(request, 'home.html', {
        'books': books,
        'edit_book': edit_book
    })


# ALL BOOKS + SEARCH
@login_required(login_url='login')
def all_books(request):
    query = request.GET.get('q')
    if query:
        books = Book.objects.filter(title__icontains=query)
    else:
        books = Book.objects.all().order_by('-created_at')

    return render(request, 'all_books.html', {'books': books})



#TOGGLE BORROW / RETURN
@login_required(login_url='login')
def toggle_borrow(request, id):
    book = Book.objects.get(id=id)

    # Borrow
    if not book.is_borrowed:
        book.is_borrowed = True
        book.borrowed_by = request.user
        book.borrowed_date = timezone.now()
        book.due_date = timezone.now() + timedelta(days=1)
        messages.success(request, "Book borrowed for 5 days 📚")

    # Return (only same user)
    elif book.borrowed_by == request.user:
        penalty = book.get_penalty()
        book.is_borrowed = False
        book.borrowed_by = None
        book.borrowed_date = None
        book.due_date = None

        if penalty > 0:
            messages.warning(request, f"Returned with penalty ₹{penalty} ⚠️")
        else:
            messages.success(request, "Book returned successfully ✅")

    else:
        messages.error(request, "Book already borrowed ❌")

    book.save()
    return redirect('all_books')

# ADD TO WISHLIST
@login_required(login_url='login')
def add_wishlist(request, id):
    book = Book.objects.get(id=id)

    obj, created = Wishlist.objects.get_or_create(user=request.user, book=book)

    if created:
        messages.success(request, "Added to wishlist ❤️")
    else:
        messages.info(request, "Already in wishlist")

    return redirect('all_books')

@login_required(login_url='login')
def remove_wishlist(request, id):
    try:
        item = Wishlist.objects.get(user=request.user, book_id=id)
        item.delete()
        messages.success(request, "Removed from wishlist ❌")
    except Wishlist.DoesNotExist:
        messages.error(request, "Item not found")

    return redirect('profile')


# PROFILE PAGE
@login_required(login_url='login')
def profile(request):
    borrowed = Book.objects.filter(borrowed_by=request.user)
    wishlist = Wishlist.objects.filter(user=request.user)

    total_price = sum(book.price for book in borrowed)

    return render(request, 'profile.html', {
        'borrowed': borrowed,
        'wishlist': wishlist,
        'total_price': total_price,
        'user': request.user
    })


# DELETE BOOK
@login_required(login_url='login')
def delete_book(request, id):
    book = Book.objects.get(id=id)
    book.delete()
    messages.success(request, "Book deleted")
    return redirect('home')