from rest_framework import serializers

def is_true(value):
    if value is not True:
        raise serializers.ValidationError(
            'This field must have a value of true if included.'
        )
