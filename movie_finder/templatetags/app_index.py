from django import template

register = template.Library()


@register.filter
def rate_active_index(sequence, position):
    return sequence[position][0]


@register.filter
def rate_dis_index(sequence, position):
    return sequence[position][1]
