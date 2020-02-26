from django.db import migrations
from backend.models import X5gonResource, X5gonUser, UserResource, Question


def forwards(apps, schema_editor):
    if schema_editor.connection.alias != 'default':
        return

    user1 = X5gonUser(name='Amal Kumar', country='India', interests='Mechanical Engineering')
    user1.save()

    user2 = X5gonUser(name='Thura Aung', country='Myanmar', interests='Engineering')
    user2.save()

    user3 = X5gonUser(name='Afi Ababio', country='Ghana', interests='Geotechnical Engineering')
    user3.save()

    user4 = X5gonUser(name='Maria José Villegas', country='Guatemala', interests='Chemical Engineering')
    user4.save()

    user5 = X5gonUser(name='Aminah Farooqi', country='Pakistan', interests='Electrical Enginering')
    user5.save()

    user6 = X5gonUser(name='Lee Choi', country='South Korea', interests='Electrical Engineering')
    user6.save()



    ur1 = UserResource(user=user1, resource=X5gonResource.objects.get(x5gon_id='112789') , crown=False , expert_on=False )
    ur1.save()

    ur2 = UserResource(user=user1, resource=X5gonResource.objects.get(x5gon_id='30289'), crown=True, expert_on=True)
    ur2.save()

    ur3 = UserResource(user=user1, resource=X5gonResource.objects.get(x5gon_id='65303'), crown=False, expert_on=False)
    ur3.save()

    ur4 = UserResource(user=user2, resource=X5gonResource.objects.get(x5gon_id='112789'), crown=True, expert_on=True)
    ur4.save()

    ur5 = UserResource(user=user2, resource=X5gonResource.objects.get(x5gon_id='30289'), crown=False, expert_on=False)
    ur5.save()

    ur6 = UserResource(user=user2, resource=X5gonResource.objects.get(x5gon_id='65303'), crown=True, expert_on=True)
    ur6.save()

    ur7 = UserResource(user=user3, resource=X5gonResource.objects.get(x5gon_id='112789'), crown=True, expert_on=True)
    ur7.save()

    ur8 = UserResource(user=user3, resource=X5gonResource.objects.get(x5gon_id='30289'), crown=True, expert_on=True)
    ur8.save()

    ur9 = UserResource(user=user3, resource=X5gonResource.objects.get(x5gon_id='65303'), crown=False, expert_on=False)
    ur9.save()

    ur10 = UserResource(user=user4, resource=X5gonResource.objects.get(x5gon_id='112789'), crown=False, expert_on=False)
    ur10.save()

    ur11 = UserResource(user=user4, resource=X5gonResource.objects.get(x5gon_id='30289'), crown=False, expert_on=False)
    ur11.save()

    ur12 = UserResource(user=user4, resource=X5gonResource.objects.get(x5gon_id='65303'), crown=False, expert_on=False)
    ur12.save()

    ur13 = UserResource(user=user5, resource=X5gonResource.objects.get(x5gon_id='112789'), crown=True, expert_on=True)
    ur13.save()

    ur14 = UserResource(user=user5, resource=X5gonResource.objects.get(x5gon_id='30289'), crown=True, expert_on=True)
    ur14.save()

    ur15 = UserResource(user=user5, resource=X5gonResource.objects.get(x5gon_id='65303'), crown=True, expert_on=True)
    ur15.save()

    ur16 = UserResource(user=user6, resource=X5gonResource.objects.get(x5gon_id='112789'), crown=False, expert_on=False)
    ur16.save()

    ur17 = UserResource(user=user6, resource=X5gonResource.objects.get(x5gon_id='30289'), crown=True, expert_on=True)
    ur17.save()

    ur18 = UserResource(user=user6, resource=X5gonResource.objects.get(x5gon_id='65303'), crown=False, expert_on=False)
    ur18.save()


    quest1 = Question(resource=X5gonResource.objects.get(x5gon_id='112789'), question='Please provide the formula for the restoring Force for small angles.', correct_answer='-(mgs)/L')
    quest1.save()

    quest2 = Question(resource=X5gonResource.objects.get(x5gon_id='112789'), question='Please provide the formula for the force constant k.', correct_answer='-(mg)/L')
    quest2.save()

    quest3 = Question(resource=X5gonResource.objects.get(x5gon_id='112789'),
                      question='By which physical concept can the pendulum be described?', correct_answer='Harmonic Oscillator')
    quest3.save()


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0002_x5gon'),
    ]

    operations = [
        migrations.RunPython(forwards),
    ]
