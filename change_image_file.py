from product.models import Color


for color in Color.objects.all():
    if color.image:
        image_name = str(color.image).split('/')[-1]
        color.image = f'colors/{image_name}'
        color.save()