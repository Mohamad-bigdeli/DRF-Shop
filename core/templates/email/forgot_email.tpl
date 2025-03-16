{% extends "mail_templated/base.tpl" %}

{% block subject %}
Forgot Password
{% endblock %}

{% block html %}
    <p>Your verification code is: <strong>{{ verification_code }}</strong></p>
    <p>This code will expire in 2 minutes.</p>
{% endblock %}