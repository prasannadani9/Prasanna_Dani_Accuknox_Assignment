from django.db import models
 
class MasterUserData(models.Model):
    email = models.CharField(primary_key= True, max_length=100)
    name = models.CharField(max_length=100)

    class Meta:
        db_table = "master_user_data"

class RelationTable(models.Model):
    email=models.CharField(primary_key= True, max_length=100)
    relation_email=models.ForeignKey(MasterUserData, to_field='email', on_delete=models.CASCADE)
    status=models.CharField(max_length=20)
   
    class Meta:
        db_table = "relation_table"