"""Profile views."""

from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.contrib import messages
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin


from checkout.models import Order
from programs.models import Program


from .models import Subscription, UserProfile
from .forms import UserProfileForm, UpdateUserForm


class ProfileView(LoginRequiredMixin, View):
    """
    View for displaying and updating user profiles.

    """
    template_name = 'profiles/profile.html'
    user_form_class = UpdateUserForm
    profile_form_class = UserProfileForm

    def get_context_data(self, **kwargs):
        """
        Retrieves context data for rendering the profile update page.
        Returns:
        - dict: A dictionary containing context data for rendering the page.
        """
        user = self.request.user
        profile = get_object_or_404(UserProfile, user=user)
        orders = profile.orders.all()

        for order in orders:
            order.total_items = 0
            for line_item in order.lineitems.all():
                order.total_items += line_item.quantity

        context = {
            "user_form": kwargs.get("user_form",
                                    self.user_form_class(instance=user)),
            "profile_form": kwargs.get(
                "profile_form", self.profile_form_class(instance=profile)
            ),
            'orders': orders,
            'on_profile_page': True,

        }
        return context

    def get(self, request):
        """
        Handles HTTP GET requests for rendering the profile update page.

        """
        context = self.get_context_data()
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        """
        Handles HTTP POST requests for updated the profile models in database.

        """
        context = self.get_context_data()
        profile = get_object_or_404(UserProfile, user=request.user)
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, instance=profile)

        # Delete user from database
        if "delete_account" in request.POST:
            try:
                user = request.user
                user.delete()
                messages.success(request, "Account Deleted.")
                return redirect("home")

            except Exception as e:
                messages.error(
                    request,
                    f"There was an error deleting your account.{e}")

            return redirect("home")

        if "user_form" in request.POST:
            if user_form.is_valid():
                user_form.save()
                context["user_form"] = user_form
                messages.success(request, 'User information updated.')
            else:
                context['user_form'] = user_form
                messages.error(request, 'Update failed. '
                               'Please ensure the forms are valid.')
                return render(request, self.template_name, context)
        else:
            if profile_form.is_valid():
                profile_form.save()
                context["profile_form"] = profile_form
                messages.success(request,
                                 'Delivery Information successfully')
            else:
                context["profile_form"] = profile_form
                messages.error(
                    request,
                    'Update failed. Please ensure the forms are valid.')

        return render(request, self.template_name, context)


class SubscriptionsView(LoginRequiredMixin, View):
    """
    View for displaying user subscriptions.

    """

    template_name = 'profiles/subscriptions.html'

    def get(self, request):
        """
        Retrieves all subscriptions from the database and orders them by price.
        If the current user has an active subscription, marks the corresponding
        subscription as 'current' in the context.
        """
        subscriptions = Subscription.objects.all().order_by('price')

        active_subscription_id = (
            request.user.profile.active_subscription.id
            if request.user.profile.active_subscription
            else None
        )
        # Add current subscription id to context
        for subscription in subscriptions:
            subscription.current = subscription.id == active_subscription_id

        context = {
            'subscriptions': subscriptions,
        }

        return render(request, self.template_name, context)


def remove_subscription(request):
    """Remove a user's active subscription."""

    redirect_url = request.POST.get('redirect_url')

    try:
        messages.success(
            request,
            f'Your {request.user.profile.active_subscription.name} '
            f'membership was cancelled'
        )
        request.user.profile.active_subscription = None
        request.user.profile.subscription = None
        request.user.profile.save()
        return redirect(redirect_url)

    except Exception as e:
        messages.error(request, f'Error unsubscribing your membership: {e}')
        return HttpResponse(status=500)


class MyCoursesView(LoginRequiredMixin, View):
    """
    View for displaying the user's courses on the "My Courses" page.
    """
    template_name = 'profiles/my_courses.html'

    def get(self, request):

        programs = []

        # Check if user has a profile and orders
        orders = request.user.profile.orders.all() or []
        for order in orders:
            for item in order.lineitems.all():
                if isinstance(item.content_object, Program):
                    programs.append(item.content_object)

        if request.user.profile.active_subscription:
            if request.user.profile.active_subscription.id == 54:
                programs = Program.objects.all()

        context = {
            'programs': programs,
        }

        return render(request, self.template_name, context)


def order_history(request, order_number):
    order = get_object_or_404(Order, order_number=order_number)

    messages.info(request, (
        f'This is a past confirmation for order number {order_number}. '
        'A confirmation email was sent on the order date.'
    ))

    template = 'checkout/checkout_success.html'
    context = {
        'order': order,
        'from_profile': True,
    }

    return render(request, template, context)
