from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    image = models.ImageField(upload_to='books/')
    price = models.FloatField(default=0)

    is_borrowed = models.BooleanField(default=False)
    borrowed_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='borrowed_books')
    due_date = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
# penalty
    def get_penalty(self):
        if self.due_date and timezone.now() > self.due_date:
            days_late = (timezone.now() - self.due_date).days
            penalty = self.price * 0.3 * days_late
            return round(penalty, 2)
        return 0


    def __str__(self):
        return self.title


# Wishlist Model
class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} - {self.book.title}"