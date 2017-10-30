from rest_framework import serializers
from .models import Task, Tasklist, Tag
from django.contrib.auth.models import User
from django.db.models import Q


#User = get_user_model()


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name',)


class TaskSerializer(serializers.ModelSerializer):
    tags = serializers.SerializerMethodField()
    #owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Task
        fields = ('id', 'name', 'description', 'completed', 'date_created', 'date_modified', 'due_date', 'priority', 'tags', 'tag',)
        read_only_fields = ('date_created', 'date_modified',)
        extra_kwargs = {"tag": {"write_only": True}}

    def get_tags(self, task):
        return task.tag.values_list('name', flat=True)


class TasklistSerializer(serializers.ModelSerializer):
    tasks = serializers.StringRelatedField(many=True)
    ownerName = serializers.ReadOnlyField(source= 'owner.username')
    sharedName = serializers.SerializerMethodField()
    sharedTasklists = serializers.SerializerMethodField()


    class Meta:
        model = Tasklist
        fields = ('id', 'name', 'tasks', 'ownerName', 'shared', 'sharedName', 'sharedTasklists')
        read_only_fields = ('tasks', )
        extra_kwargs = {"shared": {"write_only": True}}

    def get_sharedName(self, tasklist):
        return tasklist.shared.values_list('username', flat=True)

    def get_sharedTasklists(self, tasklist):
        t = Tasklist.objects.filter(shared=tasklist.owner)
        res = []
        for tt in t:
           res.append((tt.name, tt.id))
        return res



class UserCreateSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(label="Email Adress")
    email2 = serializers.EmailField(label="Confirm Email")
    class Meta:
        model = User
        fields = ('username', 'email', 'email2', 'password',)
        extra_kwargs = {"password": {"write_only": True}}

    def validate(self, data):
        #email = data["email"]
        #user_qs = User.objects.filter(email= email)
        #if user_qs.exists():
        #    raise serializers.ValidationError("User with this email has already registered")

        return data

    def validate_email(self, value):
        data = self.get_initial()
        email2 = data.get("email2")
        email1 = value
        if email1 != email2:
            raise serializers.ValidationError("Emails must match")
        user_qs = User.objects.filter(email= email1)
        if user_qs.exists():
            raise serializers.ValidationError("User with this email has already registered")

        return value

    def validate_email2(self, value):
        data = self.get_initial()
        email1 = data.get("email")
        email2 = value
        if email1 != email2:
            raise serializers.ValidationError("Emails must match")

        return value

    def create(self, validated_data):
        username = validated_data["username"]
        email = validated_data["email"]
        password = validated_data["password"]
        user_obj = User(username= username, email= email,)
        user_obj.set_password(password)
        user_obj.save()

        return validated_data


"""class UserLoginSerializer(serializers.ModelSerializer):
    token = serializers.CharField(allow_blank= True, read_only= True)
    username = serializers.CharField(required= False, allow_blank= True)
    email = serializers.EmailField(label= "Email Adress", required= False, allow_blank= True)
    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'token',)
        extra_kwargs = {"password": {"write_only": True}}

    def validate(self, data):
        user_obj = None
        email = data.get("email", None)
        username = data.get("username", None)
        password = data["password"]
        if not email and not username:
            raise serializers.ValidationError("An email or username is required to login")
        user = User.objects.filter(Q(email= email) | Q(username= username)).distinct()
        if user.exists() and user.count() == 1:
            user_obj = user.first()
        else:
            raise serializers.ValidationError("This username/email is not valid")
        if user_obj:
            if not user_obj.check_password(password):
                raise serializers.ValidationError("Incorrect password, pleaase try again")
        data["token"] = "SOME RANDOM TOKEN"

        return data"""


class UserSerializer(serializers.ModelSerializer):
    tasklists = serializers.PrimaryKeyRelatedField(many=True, queryset=Tasklist.objects.all())

    class Meta:
        model = User
        fields = ('id', 'username','email', 'tasklists')

