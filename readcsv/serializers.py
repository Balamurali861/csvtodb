from rest_framework import serializers
from .models import User
from .models import File


class Userserializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username','password','is_superuser']
        extra_kwargs = {
            'password':{'write_only':True}
        }
    def create(self, validated_data):
        password = validated_data.pop('password',None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        else:
            raise serializers.ValidationError('Some parameter is missing, Username and Password are mandatory fields')
        instance.save()
        return instance


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = "__all__"
