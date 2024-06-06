# import pytest
# from django.contrib.auth import authenticate
# from calendar_admin.bot_admin.models import User
#
#
# @pytest.mark.django_db
# def test_user_authentication():
#     User.objects.create_user(username='testuser', password='password123')
#     user = authenticate(username='testuser', password='password123')
#     assert user is not None
#     assert user.is_authenticated
