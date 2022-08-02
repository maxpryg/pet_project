# from django.contrib import admin
# from django.contrib.auth import get_user_model
#
# from blog.models import Post, Comment
#
#
# user_model = get_user_model()
#
#
# class DashboardAdminSite(admin.AdminSite):
#     def each_context(self, request):
#         context = super().each_context(request)
#         context.update({
#             'total_users': user_model.objects.count(),
#             'total_posts': Post.objects.count(),
#             'total_comments': Comment.objects.count()
# #             'total_likes': Post.likes.count(),
# #             'registered_per_week': user_model.registered_per_week(),
#         })
#         return context
#
