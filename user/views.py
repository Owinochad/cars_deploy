from django.shortcuts import render, redirect, HttpResponse, get_object_or_404

from .forms import UserUpdateForm, ProfileUpdateForm  # Assuming these forms are correctly defined
from django.contrib.auth.decorators import login_required
from competition.models  import *
from .models import *

import json

from django.http import HttpResponse

import requests
import time
from competition.credentials import LipanaMpesaPpassword, MpesaAccessToken, MpesaC2bCredential
from django.contrib import messages
import logging
from decimal import Decimal
from django.utils import timezone


def ticket_view(request, competition_id):
    user = request.user

    # Check if the competition is a regular or a holiday competition
    try:
        competition = Competition.objects.get(id=competition_id)
        tickets = Ticket.objects.filter(user=user, competition=competition)
        competition_type = 'competition'
    except Competition.DoesNotExist:
        try:
            holiday = HolidayCompetition.objects.get(id=competition_id)
            tickets = Ticket.objects.filter(user=user, holiday=holiday)
            competition_type = 'holiday'
        except HolidayCompetition.DoesNotExist:
            # Handle the case where neither competition exists
            return redirect('some-error-view')  # Redirect or show an error

    context = {
        'competition': competition if competition_type == 'competition' else holiday,
        'tickets': tickets,
        'competition_type': competition_type,
    }

    return render(request, 'user/ticketview.html', context)

# @login_required
# def profile(request):
#     user = request.user

#     # Fetch a subset of regular competitions and holiday competitions
#     competition = Competition.objects.all()[:2]  # Adjust filter as needed
#     holiday_competition = HolidayCompetition.objects.first()

#     # Query all tickets associated with this user, including both regular and holiday competitions
#     tickets = Ticket.objects.filter(user=user).select_related('competition', 'holiday')

#     # Group tickets by both competition and holiday competition
#     competitions = {}
#     holidays = {}
    
#     for ticket in tickets:
#         if ticket.competition:
#             if ticket.competition not in competitions:
#                 competitions[ticket.competition] = []
#             competitions[ticket.competition].append(ticket.number)
#         elif ticket.holiday:
#             if ticket.holiday not in competitions:
#                 holidays[ticket.holiday] = []
#             holidays[ticket.holiday].append(ticket.number)

#     return render(request, 'user/profile.html', {
#         'user': user,
#         'competitions': competitions,
#         'competition': competition,
#         'holiday': holiday_competition,
#         'holidays':holidays,
#     })

@login_required
def profile(request):
    user = request.user

    # Fetch competitions
    competitions = Competition.objects.all()[:2]  # Car competitions
    holiday_competition = HolidayCompetition.objects.first()

    # Query all tickets associated with this user, including both regular and holiday competitions
    tickets = Ticket.objects.filter(user=user).select_related('competition', 'holiday')

    # Group tickets by both competition and holiday competition
    competitions_dict = {}
    holidays_dict = {}
    
    for ticket in tickets:
        if ticket.competition:
            if ticket.competition not in competitions_dict:
                competitions_dict[ticket.competition] = []
            competitions_dict[ticket.competition].append(ticket.number)
        elif ticket.holiday:
            if ticket.holiday not in holidays_dict:
                holidays_dict[ticket.holiday] = []
            holidays_dict[ticket.holiday].append(ticket.number)

    return render(request, 'user/profile.html', {
        'user': user,
        'competitions': competitions_dict,
        'competition': competitions,
        'holiday': holiday_competition,
        'holidays': holidays_dict,
    })



@login_required
def profile_update(request):

    competition = Competition.objects.all()[:2]  # Adjust filter as needed
    holiday_competition = HolidayCompetition.objects.first()
    

    if not hasattr(request.user, 'userprofile'):
        UserProfile.objects.create(user=request.user)
    
    user_profile = request.user.userprofile

    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=user_profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('user-profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.userprofile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'competition': competition,
        'holiday_competition': holiday_competition,
    }
    return render(request, 'user/profile_update.html', context)


logger = logging.getLogger(__name__)

@login_required
def deposit(request):
    wallet = get_object_or_404(Wallet, user=request.user)

    if request.method == 'POST':
        amount = request.POST.get('amount')

        try:
            # Ensure that amount is a valid decimal
            if amount:
                amount = Decimal(amount)
                
                if amount > 0:
                    # Update wallet balance and create a transaction
                    wallet.update_balance(amount, 'Deposit')

                    # Feedback to user
                    messages.success(request, f"{amount} KES deposited successfully!")

                    # Redirect after successful deposit
                    return redirect('deposit')
                else:
                    messages.error(request, "The deposit amount must be greater than 0.")
            else:
                messages.error(request, "Please provide a valid amount.")

        except Exception as e:
            messages.error(request, f"Error processing deposit: {str(e)}")
            logger.error(f"Error during deposit: {str(e)}")

    # Fetch the transactions for the user
    transactions = Transaction.objects.filter(user=request.user).order_by('-date')

    context = {
        'wallet': wallet,
        'transactions': transactions,
    }
    return render(request, 'user/deposit.html', context)
    

def deposit_stk(request):
    if not request.user.is_authenticated:
        return HttpResponse("Unauthorized", status=401)

    if request.method == "POST":
        phone = request.POST.get('phone')
        amount = request.POST.get('amount')
        access_token = MpesaAccessToken.get_access_token()

        print(type(phone), type(amount))

        if not access_token:
            return HttpResponse("Failed to get access token.", status=500)

        api_url = MpesaC2bCredential.api_url
        headers = {"Authorization": f"Bearer {access_token}"}
        request_data = {
            "BusinessShortCode": LipanaMpesaPpassword.business_short_code,
            "Password": LipanaMpesaPpassword.decode_password,
            "Timestamp": LipanaMpesaPpassword.lipa_time,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": amount,
            "PartyA": phone,
            "PartyB": LipanaMpesaPpassword.business_short_code,
            "PhoneNumber": phone,
            "CallBackURL": "https://django-daraja.vercel.app/add-payment/",
            "AccountReference": "Dream Car",
            "TransactionDesc": "Web Development Charges"
        }

        response = requests.post(api_url, json=request_data, headers=headers)
        response_data = json.loads(response.text)

        print("Response data from M-Pesa API:", response_data)
        checkout_request_id = response_data.get('CheckoutRequestID')

        if response_data.get('ResponseCode') == '0':
            time.sleep(20)  # Simulate a delay for the user to complete the payment

            # Fetch the list of transactions from the callback endpoint
            callback_response = requests.get("https://django-daraja.vercel.app/payments/")
            callback_data = json.loads(callback_response.text)
            callback_data_list = callback_data["payments"]["rows"]

            # Loop through the callback_data_list to check if the provided checkout_request_id exists
            found = False  # Flag to indicate if we found the ID

            for transaction in callback_data_list:
                if transaction.get("checkoutrequestid") == checkout_request_id:
                    found = True
                    print(f"Checkout Request ID {checkout_request_id} found in the list.")

                    # If transaction was successful
                    if transaction.get("resultcode") == 0:     
                        # Update wallet balance
                        wallet = Wallet.objects.get(user=request.user)  # Retrieve the user's wallet
                        wallet.amount += int(amount)  # Add the provided amount to the current wallet amount
                        wallet.save()  # Save the updated wallet instance

                        # **Create the transaction record in the database**
                        Transaction.objects.create(
                            user=request.user,
                            transaction_type="Deposit",
                            amount=Decimal(amount),  # Make sure it's stored as a Decimal
                            date=timezone.now()  # Add a timestamp
                        )

                        messages.success(request, f"{amount} KES deposited successfully!")
                        return redirect('deposit')
                    else:
                         # Update wallet balance
                        wallet = Wallet.objects.get(user=request.user)  # Retrieve the user's wallet
                        wallet.amount += int(amount)  # Add the provided amount to the current wallet amount
                        wallet.save()  # Save the updated wallet instance

                        # **Create the transaction record in the database**
                        Transaction.objects.create(
                            user=request.user,
                            transaction_type="Deposit",
                            amount=Decimal(amount),  # Make sure it's stored as a Decimal
                            date=timezone.now()  # Add a timestamp
                        )
                        messages.error(request, "Transaction failed or was canceled.")
                        return redirect('deposit') 
                            
            if not found:
                print(f"Checkout Request ID {checkout_request_id} not found in the list.")
                messages.error(request, "Transaction not found in M-Pesa records.")

        else:
            messages.error(request, "Failed to initiate transaction with M-Pesa.")
            return redirect('check_out')

    return HttpResponse("Invalid request method.", status=405)