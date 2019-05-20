from django.contrib.auth.models import Group
from vk_sender.tasks import send_vk_message, send_vk_message_with_photos

def make_a_mailing(ad):
    try:
        group = Group.objects.get(name=ad.category)
    except:
        group = None

    notification_text = '''Новое объявление в категории {0}!
                           Автор - {1}
                           {2}
                           {3}
                        '''.format(ad.category, ad.seller.get_full_name, ad.header, ad.text)

    vk_method = send_vk_message_with_photos if ad.image else send_vk_message
    if (group is not None):
        for user in group.user_set.all():
            vk_method(user_id=user.id, message=notification_text, photo=ad.image)
