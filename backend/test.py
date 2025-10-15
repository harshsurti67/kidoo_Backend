# # import cloudinary
# # import cloudinary.uploader
# # import os

# # cloudinary.config(
# #   cloud_name = "diadyznqa",
# #   api_key = "643916278533495",
# #   api_secret = "mljiWucEv3eiH6wFlj2aJ2_M0lY"
# # )

# # media_folder = "media"  # your local media folder

# # for root, dirs, files in os.walk(media_folder):
# #     for file in files:
# #         file_path = os.path.join(root, file)
# #         result = cloudinary.uploader.upload(file_path)
# #         print(result['secure_url'])
# import os
# import django
# import cloudinary.uploader

# # Setup Django environment
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "kidoo_preschool.settings")
# django.setup()

# cloudinary.config(
#   cloud_name = "diadyznqa",
#   api_key = "643916278533495",
#   api_secret = "mljiWucEv3eiH6wFlj2aJ2_M0lY"
# )


# from api.models import Program, Gallery, Testimonial, Event, Blog, TeamMember, HomeSlider

# def migrate_image_field(model, field_name):
#     """
#     Upload images from local storage to Cloudinary and update model field
#     """
#     instances = model.objects.all()
#     for obj in instances:
#         image_field = getattr(obj, field_name)
#         if image_field and not str(image_field).startswith('http'):
#             try:
#                 print(f"Uploading {model.__name__} id={obj.id}...")
#                 image_field.open()
#                 result = cloudinary.uploader.upload(image_field.file)
#                 setattr(obj, field_name, result['secure_url'])
#                 obj.save()
#                 print(f"Uploaded: {result['secure_url']}")
#             except Exception as e:
#                 print(f"Error uploading {model.__name__} id={obj.id}: {e}")

# def migrate_all():
#     print("Migrating Program images...")
#     migrate_image_field(Program, 'image')

#     print("Migrating Gallery images...")
#     migrate_image_field(Gallery, 'image')

#     print("Migrating Testimonial photos...")
#     migrate_image_field(Testimonial, 'photo')

#     print("Migrating Event images...")
#     migrate_image_field(Event, 'image')

#     print("Migrating Blog images...")
#     migrate_image_field(Blog, 'image')

#     print("Migrating TeamMember photos...")
#     migrate_image_field(TeamMember, 'photo')

#     print("Migrating HomeSlider images...")
#     migrate_image_field(HomeSlider, 'image')
#     migrate_image_field(HomeSlider, 'video_poster')  # optional poster image

# if __name__ == "__main__":
#     migrate_all()
#     print("Migration completed!")
from api.models import HomeSlider

for h in HomeSlider.objects.all():
    print(h.image)        # Cloudinary URL
    print(h.video_poster) # Cloudinary URL
    print(h.video)        # Cloudinary URL or None
