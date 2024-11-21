
from django.db import models, transaction
from django.db.models import F
import random

# Create your models here.
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import InMemoryUploadedFile
from io import BytesIO
from pillow import *
from django.db.models import Q
from django.db.models import UniqueConstraint
from django.db.models import Sum


User = get_user_model()


class MpesaTransaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    merchant_request_id = models.CharField(max_length=255, null=True)
    checkout_request_id = models.CharField(max_length=255, null=True)
    result_code = models.IntegerField(null=True)
    result_desc = models.CharField(max_length=255, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    mpesa_receipt_number = models.CharField(max_length=255, null=True)
    transaction_date = models.DateTimeField(null=True)
    phone_number = models.CharField(max_length=15, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.mpesa_receipt_number}"


class Competition(models.Model):
    car_model = models.CharField(max_length=100)
    car_make = models.CharField(max_length=100, default='one')
    specifications = models.TextField()
    image = models.ImageField(upload_to='cars/')
    ticket_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_tickets = models.PositiveIntegerField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    tickets_sold = models.IntegerField(default=0)

    index_display = models.BooleanField(default=False, help_text="Show on index page")
    priority = models.PositiveSmallIntegerField(
        choices=[(i, f"Priority {i}") for i in range(1, 5)],
        unique=True, blank=True, null=True,
        help_text="Set priority from 1-4 for index page display order"
    )

    def total_ticket_sold(self):
        return self.tickets_sold.count()

    def remaining_tickets(self):
        return self.total_tickets - self.total_ticket_sold()
    
    def save(self, *args, **kwargs):
        if self.image:
            self.image = process_image(self.image)  # Call the image processing function
        super(Competition, self).save(*args, **kwargs)

    def tickets_sold_percentage(self):
        if self.total_tickets > 0:
            percentage = (self.tickets_sold / self.total_tickets) * 100
            return max(percentage, 10)
        return 10  # Return 0 if there are no total tickets available
    
    def days_rem(self):
        if self.end_date:
            return(self.end_date - self.start_date).days        


    def __str__(self):
        return self.car_model
    

    
class CompetitionImage(models.Model):
    competition = models.ForeignKey(Competition, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='cars/')

    def __str__(self):
        return f"Image for {self.competition.car_model}"
    
    def save(self, *args, **kwargs):
        if self.image:
            self.image = processimage(self.image)
        super().save(*args, **kwargs)
    

class HolidayCompetition(models.Model):

    class CategoryChoices(models.TextChoices):
        HOLIDAY = 'holiday', 'Holiday'
        ELECTRONICS = 'electronics', 'Electronics'

    name = models.CharField(max_length=100, default='diani')
    description = models.TextField()
    image = models.ImageField(upload_to='cars/')
    ticket_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_tickets = models.PositiveIntegerField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    tickets_sold = models.IntegerField(default=0)

    category = models.CharField(
        max_length=20,
        choices=CategoryChoices.choices,
        default=CategoryChoices.HOLIDAY,
        help_text="Select the competition category"
    )

    index_display = models.BooleanField(default=False, help_text="Show on index page")
    priority = models.PositiveSmallIntegerField(
        choices=[(i, f"Priority {i}") for i in range(1, 5)],
        unique=True, blank=True, null=True,
        help_text="Set priority from 1-4 for index page display order"
    )

    def total_ticket_sold(self):
        return self.tickets_sold.count()

    def remaining_tickets(self):
        return self.total_tickets - self.total_ticket_sold()
    
    def save(self, *args, **kwargs):
        if self.image:
            self.image = process_image(self.image)  # Call the image processing function
        super(HolidayCompetition, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.get_category_display()})"
        
    
    def tickets_sold_percentage(self):
        if self.total_tickets > 0:
            percentage = (self.tickets_sold / self.total_tickets) * 100
            return max(percentage, 10)
        return 10  # Return 0 if there are no total tickets available
    
    def days_rem(self):
        if self.end_date:
            return(self.end_date - self.start_date).days
    
class HoliCompetitionImage(models.Model):
    competition = models.ForeignKey(HolidayCompetition, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='cars/')

    def __str__(self):
        return f"Image for {self.competition.name}"
    
    def save(self, *args, **kwargs):
        if self.image:
            self.image = processimage(self.image)
        super().save(*args, **kwargs)

    

class Ticket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE, null=True, blank=True)
    holiday = models.ForeignKey(HolidayCompetition, on_delete=models.CASCADE, null=True, blank=True)
    number = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    @staticmethod
    def generate_ticket_number(competition_or_holiday):
        # Ensure the current state of tickets_sold is fetched
        competition_or_holiday.refresh_from_db()
        
        total_tickets = competition_or_holiday.total_tickets
        tickets_sold = competition_or_holiday.tickets_sold
        
        if tickets_sold >= total_tickets:
            raise ValueError("No more tickets available for this competition or holiday.")

        # Fetch used ticket numbers
        used_numbers = Ticket.objects.filter(
            competition=competition_or_holiday if isinstance(competition_or_holiday, Competition) else None,
            holiday=competition_or_holiday if isinstance(competition_or_holiday, HolidayCompetition) else None
        ).values_list('number', flat=True)

        # Compute available ticket numbers
        available_numbers = set(range(1, total_tickets + 1)) - set(used_numbers)

        if not available_numbers:
            raise ValueError("No available ticket numbers left.")

        # Randomly select a ticket number from the available pool
        return random.choice(list(available_numbers))

    def __str__(self):
        if self.competition:
            return f"{self.user.username} - {self.competition.car_model} - {self.number} - {self.created_at}"
        elif self.holiday:
            return f"{self.user.username} - {self.holiday.name} - {self.number} - {self.created_at}"
        return f"{self.user.username} - No Competition"

class Entry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    competition = models.ForeignKey(Competition, related_name='entries', on_delete=models.CASCADE, null=True, blank=True)
    holiday = models.ForeignKey(HolidayCompetition, related_name='entries', on_delete=models.CASCADE, null=True, blank=True)
    purchase_date = models.DateTimeField(auto_now_add=True)
    quantity = models.PositiveIntegerField(default=1)  # Track number of tickets purchased

    def save(self, *args, **kwargs):
        if not self.pk:  # Only run on creation
            competition_or_holiday = self.competition or self.holiday
            print(f"Attempting to generate {self.quantity} ticket(s) for {competition_or_holiday}")

            try:
                with transaction.atomic():
                    # Check the current sold tickets for the competition or holiday
                    current_tickets_sold = Ticket.objects.filter(
                        competition=competition_or_holiday if isinstance(competition_or_holiday, Competition) else None,
                        holiday=competition_or_holiday if isinstance(competition_or_holiday, HolidayCompetition) else None
                    ).aggregate(total=Sum('number'))['total'] or 0
                    
                    # Ensure there are enough tickets available
                    if current_tickets_sold + self.quantity > competition_or_holiday.total_tickets:
                        raise ValueError("Not enough tickets available.")

                    # Create tickets
                    for _ in range(self.quantity):
                        ticket_number = Ticket.generate_ticket_number(competition_or_holiday)
                        Ticket.objects.create(user=self.user, competition=self.competition, holiday=self.holiday, number=ticket_number)

                    # Update tickets sold only once based on the quantity purchased
                    competition_or_holiday.tickets_sold = F('tickets_sold') + self.quantity
                    competition_or_holiday.save(update_fields=['tickets_sold'])

            except ValueError as e:
                print(f"Error generating ticket number: {e}")

        super().save(*args, **kwargs)

    def __str__(self):
        if self.competition:
            return f"{self.user.username} - {self.competition.car_model}"
        elif self.holiday:
            return f"{self.user.username} - {self.holiday.name}"
        return f"{self.user.username} - No Competition"
    
class Winner(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE, null=True, blank=True)
    holiday = models.ForeignKey(HolidayCompetition, on_delete=models.CASCADE, null=True, blank=True)
    win_date = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='winners/', blank=True, null=True)
    testimonial = models.TextField(blank=True, null=True)

    def __str__(self):
        # Check whether this winner is linked to a car competition or a holiday competition
        if self.competition:
            return f"{self.user.username} - {self.competition.car_model} (Car Competition)"
        elif self.holiday:
            return f"{self.user.username} - {self.holiday.name} (Holiday Competition)"
        else:
            return f"{self.user.username} - Unknown Competition"


class ContactInquiry(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.subject

class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    published_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class FAQ(models.Model):
    question = models.CharField(max_length=200)
    answer = models.TextField()

    def __str__(self):
        return self.question

class BasketItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE, null=True, blank=True)
    holicompetition = models.ForeignKey(HolidayCompetition, on_delete=models.CASCADE, null=True, blank=True)
    ticket_count = models.PositiveIntegerField(default=1)

    class Meta:
        constraints = [
            UniqueConstraint(fields=['user', 'competition'], name='unique_user_competition', condition=Q(competition__isnull=False)),
            UniqueConstraint(fields=['user', 'holicompetition'], name='unique_user_holicompetition', condition=Q(holicompetition__isnull=False))
        ]

    def __str__(self):
        if self.competition:
            return f"{self.ticket_count} tickets for {self.competition.car_model}"
        elif self.holicompetition:
            return f"{self.ticket_count} tickets for {self.holicompetition.name}"
        return f"{self.ticket_count} tickets"
    
    def save(self, *args, **kwargs):
        if self.ticket_count < 0:
            raise ValueError("Ticket count cannot be negative.")
        super().save(*args, **kwargs)
