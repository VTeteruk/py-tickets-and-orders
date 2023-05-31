from datetime import datetime

from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, Ticket, User, MovieSession


@transaction.atomic
def create_order(
        tickets: list[dict],
        username: str,
        date: datetime = None
) -> None:
    new_order = Order.objects.create(user=User.objects.get(username=username))
    if date:
        new_order.created_at = date
        new_order.save()

    for ticket in tickets:
        Ticket.objects.create(
            movie_session=MovieSession.objects.get(
                id=ticket.get("movie_session")
            ),
            order=new_order,
            row=ticket.get("row"),
            seat=ticket.get("seat")
        )


def get_orders(username: str = None) -> QuerySet:
    if username:
        return Order.objects.filter(user__username=username)
    return Order.objects.all()