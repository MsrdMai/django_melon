from django.db import models
# Create your models here.
from django.contrib.auth.models import User

class TypeUser(models.Model):
    id = models.AutoField(primary_key=True)
    type_name = models.CharField(max_length=50)
    class Meta:
        managed = True
        db_table = "type_user"
    def __str__(self):
        return self.type_name

    # TypeUser = (
    #     (เจ้าของฟาร์ม),
    #     (ผู้ซื้อออนไลน์),
    # )



class UserInType(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.OneToOneField(User, on_delete=models.CASCADE)
    Typeuser_id = models.ForeignKey(TypeUser, on_delete=models.CASCADE)
    class Meta:
        managed = True
        db_table = "UserInType"
