# Generated by Django 3.2.4 on 2021-07-15 04:13

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import mvpsite.models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=32, verbose_name='Address: ')),
                ('address_2', models.CharField(blank=True, max_length=32, verbose_name='Address Line 2: ')),
                ('state', models.CharField(max_length=32, verbose_name='State/Province: ')),
                ('city', models.CharField(max_length=32, verbose_name='City: ')),
                ('country', models.CharField(choices=[('AF', 'Afghanistan'), ('AL', 'Albania'), ('DZ', 'Algeria'), ('AS', 'American Samoa'), ('AD', 'Andorra'), ('AO', 'Angola'), ('AI', 'Anguilla'), ('AQ', 'Antarctica'), ('AG', 'Antigua & Barbuda'), ('AR', 'Argentina'), ('AM', 'Armenia'), ('AW', 'Aruba'), ('AU', 'Australia'), ('AT', 'Austria'), ('AZ', 'Azerbaijan'), ('BS', 'Bahama'), ('BH', 'Bahrain'), ('BD', 'Bangladesh'), ('BB', 'Barbados'), ('BY', 'Belarus'), ('BE', 'Belgium'), ('BZ', 'Belize'), ('BJ', 'Benin'), ('BM', 'Bermuda'), ('BT', 'Bhutan'), ('BO', 'Bolivia'), ('BA', 'Bosnia and Herzegovina'), ('BW', 'Botswana'), ('BV', 'Bouvet Island'), ('BR', 'Brazil'), ('IO', 'British Indian Ocean Territory'), ('VG', 'British Virgin Islands'), ('BN', 'Brunei Darussalam'), ('BG', 'Bulgaria'), ('BF', 'Burkina Faso'), ('BU', 'Burma (no longer exists)'), ('BI', 'Burundi'), ('KH', 'Cambodia'), ('CM', 'Cameroon'), ('CA', 'Canada'), ('CV', 'Cape Verde'), ('KY', 'Cayman Islands'), ('CF', 'Central African Republic'), ('TD', 'Chad'), ('CL', 'Chile'), ('CN', 'China'), ('CX', 'Christmas Island'), ('CC', 'Cocos (Keeling) Islands'), ('CO', 'Colombia'), ('KM', 'Comoros'), ('CG', 'Congo'), ('CK', 'Cook Islands'), ('CR', 'Costa Rica'), ('CI', "CÃ´te D'ivoire (Ivory Coast)"), ('HR', 'Croatia'), ('CU', 'Cuba'), ('CY', 'Cyprus'), ('CZ', 'Czech Republic'), ('CS', 'Czechoslovakia (no longer exists)'), ('YD', 'Democratic Yemen (no longer exists)'), ('DK', 'Denmark'), ('DJ', 'Djibouti'), ('DM', 'Dominica'), ('DO', 'Dominican Republic'), ('TP', 'East Timor'), ('EC', 'Ecuador'), ('EG', 'Egypt'), ('SV', 'El Salvador'), ('GQ', 'Equatorial Guinea'), ('ER', 'Eritrea'), ('EE', 'Estonia'), ('ET', 'Ethiopia'), ('FK', 'Falkland Islands (Malvinas)'), ('FO', 'Faroe Islands'), ('FJ', 'Fiji'), ('FI', 'Finland'), ('FR', 'France'), ('FX', 'France, Metropolitan'), ('GF', 'French Guiana'), ('PF', 'French Polynesia'), ('TF', 'French Southern Territories'), ('GA', 'Gabon'), ('GM', 'Gambia'), ('GE', 'Georgia'), ('DD', 'German Democratic Republic (no longer exists)'), ('DE', 'Germany'), ('GH', 'Ghana'), ('GI', 'Gibraltar'), ('GR', 'Greece'), ('GL', 'Greenland'), ('GD', 'Grenada'), ('GP', 'Guadeloupe'), ('GU', 'Guam'), ('GT', 'Guatemala'), ('GN', 'Guinea'), ('GW', 'Guinea-Bissau'), ('GY', 'Guyana'), ('HT', 'Haiti'), ('HM', 'Heard &amp; McDonald Islands'), ('HN', 'Honduras'), ('HK', 'Hong Kong'), ('HU', 'Hungary'), ('IS', 'Iceland'), ('IN', 'India'), ('ID', 'Indonesia'), ('IQ', 'Iraq'), ('IE', 'Ireland'), ('IR', 'Islamic Republic of Iran'), ('IL', 'Israel'), ('IT', 'Italy'), ('JM', 'Jamaica'), ('JP', 'Japan'), ('JO', 'Jordan'), ('KZ', 'Kazakhstan'), ('KE', 'Kenya'), ('KI', 'Kiribati'), ('KP', "Korea, Democratic People's Republic of"), ('KR', 'Korea, Republic of'), ('KW', 'Kuwait'), ('KG', 'Kyrgyzstan'), ('LA', "Lao People's Democratic Republic"), ('LV', 'Latvia'), ('LB', 'Lebanon'), ('LS', 'Lesotho'), ('LR', 'Liberia'), ('LY', 'Libyan Arab Jamahiriya'), ('LI', 'Liechtenstein'), ('LT', 'Lithuania'), ('LU', 'Luxembourg'), ('MO', 'Macau'), ('MG', 'Madagascar'), ('MW', 'Malawi'), ('MY', 'Malaysia'), ('MV', 'Maldives'), ('ML', 'Mali'), ('MT', 'Malta'), ('MH', 'Marshall Islands'), ('MQ', 'Martinique'), ('MR', 'Mauritania'), ('MU', 'Mauritius'), ('YT', 'Mayotte'), ('MX', 'Mexico'), ('FM', 'Micronesia'), ('MD', 'Moldova, Republic of'), ('MC', 'Monaco'), ('MN', 'Mongolia'), ('MS', 'Monserrat'), ('MA', 'Morocco'), ('MZ', 'Mozambique'), ('MM', 'Myanmar'), ('NA', 'Nambia'), ('NR', 'Nauru'), ('NP', 'Nepal'), ('NL', 'Netherlands'), ('AN', 'Netherlands Antilles'), ('NT', 'Neutral Zone (no longer exists)'), ('NC', 'New Caledonia'), ('NZ', 'New Zealand'), ('NI', 'Nicaragua'), ('NE', 'Niger'), ('NG', 'Nigeria'), ('NU', 'Niue'), ('NF', 'Norfolk Island'), ('MP', 'Northern Mariana Islands'), ('NO', 'Norway'), ('OM', 'Oman'), ('PK', 'Pakistan'), ('PW', 'Palau'), ('PA', 'Panama'), ('PG', 'Papua New Guinea'), ('PY', 'Paraguay'), ('PE', 'Peru'), ('PH', 'Philippines'), ('PN', 'Pitcairn'), ('PL', 'Poland'), ('PT', 'Portugal'), ('PR', 'Puerto Rico'), ('QA', 'Qatar'), ('RE', 'RÃ©union'), ('RO', 'Romania'), ('RU', 'Russian Federation'), ('RW', 'Rwanda'), ('LC', 'Saint Lucia'), ('WS', 'Samoa'), ('SM', 'San Marino'), ('ST', 'Sao Tome &amp; Principe'), ('SA', 'Saudi Arabia'), ('SN', 'Senegal'), ('SC', 'Seychelles'), ('SL', 'Sierra Leone'), ('SG', 'Singapore'), ('SK', 'Slovakia'), ('SI', 'Slovenia'), ('SB', 'Solomon Islands'), ('SO', 'Somalia'), ('ZA', 'South Africa'), ('GS', 'South Georgia and the South Sandwich Islands'), ('ES', 'Spain'), ('LK', 'Sri Lanka'), ('SH', 'St. Helena'), ('KN', 'St. Kitts and Nevis'), ('PM', 'St. Pierre & Miquelon'), ('VC', 'St. Vincent & the Grenadines'), ('SD', 'Sudan'), ('SR', 'Suriname'), ('SJ', 'Svalbard & Jan Mayen Islands'), ('SZ', 'Swaziland'), ('SE', 'Sweden'), ('CH', 'Switzerland'), ('SY', 'Syrian Arab Republic'), ('TW', 'Taiwan, Province of China'), ('TJ', 'Tajikistan'), ('TZ', 'Tanzania, United Republic of'), ('TH', 'Thailand'), ('TG', 'Togo'), ('TK', 'Tokelau'), ('TO', 'Tonga'), ('TT', 'Trinidad &amp; Tobago'), ('TN', 'Tunisia'), ('TR', 'Turkey'), ('TM', 'Turkmenistan'), ('TC', 'Turks &amp; Caicos Islands'), ('TV', 'Tuvalu'), ('UG', 'Uganda'), ('UA', 'Ukraine'), ('SU', 'Union of Soviet Socialist Republics (no longer exi'), ('AE', 'United Arab Emirates'), ('GB', 'United Kingdom (Great Britain)'), ('UM', 'United States Minor Outlying Islands'), ('US', 'United States of America'), ('VI', 'United States Virgin Islands'), ('ZZ', 'Unknown or unspecified country'), ('UY', 'Uruguay'), ('UZ', 'Uzbekistan'), ('VU', 'Vanuatu'), ('VA', 'Vatican City State (Holy See)'), ('VE', 'Venezuela'), ('VN', 'Vietnam'), ('WF', 'Wallis & Futuna Islands'), ('EH', 'Western Sahara'), ('YE', 'Yemen'), ('YU', 'Yugoslavia'), ('ZR', 'Zaire'), ('ZM', 'Zambia'), ('ZW', 'Zimbabwe')], max_length=2, verbose_name='Country: ')),
                ('postal_code', models.CharField(max_length=32, verbose_name='Postal Code: ')),
            ],
        ),
        migrations.CreateModel(
            name='CourierAd',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('package_weight', models.FloatField(verbose_name='Maximum weight (lb): ')),
                ('package_price_min', models.FloatField(verbose_name='Price (USD): ')),
                ('dep_country', models.CharField(choices=[('AF', 'Afghanistan'), ('AL', 'Albania'), ('DZ', 'Algeria'), ('AS', 'American Samoa'), ('AD', 'Andorra'), ('AO', 'Angola'), ('AI', 'Anguilla'), ('AQ', 'Antarctica'), ('AG', 'Antigua & Barbuda'), ('AR', 'Argentina'), ('AM', 'Armenia'), ('AW', 'Aruba'), ('AU', 'Australia'), ('AT', 'Austria'), ('AZ', 'Azerbaijan'), ('BS', 'Bahama'), ('BH', 'Bahrain'), ('BD', 'Bangladesh'), ('BB', 'Barbados'), ('BY', 'Belarus'), ('BE', 'Belgium'), ('BZ', 'Belize'), ('BJ', 'Benin'), ('BM', 'Bermuda'), ('BT', 'Bhutan'), ('BO', 'Bolivia'), ('BA', 'Bosnia and Herzegovina'), ('BW', 'Botswana'), ('BV', 'Bouvet Island'), ('BR', 'Brazil'), ('IO', 'British Indian Ocean Territory'), ('VG', 'British Virgin Islands'), ('BN', 'Brunei Darussalam'), ('BG', 'Bulgaria'), ('BF', 'Burkina Faso'), ('BU', 'Burma (no longer exists)'), ('BI', 'Burundi'), ('KH', 'Cambodia'), ('CM', 'Cameroon'), ('CA', 'Canada'), ('CV', 'Cape Verde'), ('KY', 'Cayman Islands'), ('CF', 'Central African Republic'), ('TD', 'Chad'), ('CL', 'Chile'), ('CN', 'China'), ('CX', 'Christmas Island'), ('CC', 'Cocos (Keeling) Islands'), ('CO', 'Colombia'), ('KM', 'Comoros'), ('CG', 'Congo'), ('CK', 'Cook Islands'), ('CR', 'Costa Rica'), ('CI', "CÃ´te D'ivoire (Ivory Coast)"), ('HR', 'Croatia'), ('CU', 'Cuba'), ('CY', 'Cyprus'), ('CZ', 'Czech Republic'), ('CS', 'Czechoslovakia (no longer exists)'), ('YD', 'Democratic Yemen (no longer exists)'), ('DK', 'Denmark'), ('DJ', 'Djibouti'), ('DM', 'Dominica'), ('DO', 'Dominican Republic'), ('TP', 'East Timor'), ('EC', 'Ecuador'), ('EG', 'Egypt'), ('SV', 'El Salvador'), ('GQ', 'Equatorial Guinea'), ('ER', 'Eritrea'), ('EE', 'Estonia'), ('ET', 'Ethiopia'), ('FK', 'Falkland Islands (Malvinas)'), ('FO', 'Faroe Islands'), ('FJ', 'Fiji'), ('FI', 'Finland'), ('FR', 'France'), ('FX', 'France, Metropolitan'), ('GF', 'French Guiana'), ('PF', 'French Polynesia'), ('TF', 'French Southern Territories'), ('GA', 'Gabon'), ('GM', 'Gambia'), ('GE', 'Georgia'), ('DD', 'German Democratic Republic (no longer exists)'), ('DE', 'Germany'), ('GH', 'Ghana'), ('GI', 'Gibraltar'), ('GR', 'Greece'), ('GL', 'Greenland'), ('GD', 'Grenada'), ('GP', 'Guadeloupe'), ('GU', 'Guam'), ('GT', 'Guatemala'), ('GN', 'Guinea'), ('GW', 'Guinea-Bissau'), ('GY', 'Guyana'), ('HT', 'Haiti'), ('HM', 'Heard &amp; McDonald Islands'), ('HN', 'Honduras'), ('HK', 'Hong Kong'), ('HU', 'Hungary'), ('IS', 'Iceland'), ('IN', 'India'), ('ID', 'Indonesia'), ('IQ', 'Iraq'), ('IE', 'Ireland'), ('IR', 'Islamic Republic of Iran'), ('IL', 'Israel'), ('IT', 'Italy'), ('JM', 'Jamaica'), ('JP', 'Japan'), ('JO', 'Jordan'), ('KZ', 'Kazakhstan'), ('KE', 'Kenya'), ('KI', 'Kiribati'), ('KP', "Korea, Democratic People's Republic of"), ('KR', 'Korea, Republic of'), ('KW', 'Kuwait'), ('KG', 'Kyrgyzstan'), ('LA', "Lao People's Democratic Republic"), ('LV', 'Latvia'), ('LB', 'Lebanon'), ('LS', 'Lesotho'), ('LR', 'Liberia'), ('LY', 'Libyan Arab Jamahiriya'), ('LI', 'Liechtenstein'), ('LT', 'Lithuania'), ('LU', 'Luxembourg'), ('MO', 'Macau'), ('MG', 'Madagascar'), ('MW', 'Malawi'), ('MY', 'Malaysia'), ('MV', 'Maldives'), ('ML', 'Mali'), ('MT', 'Malta'), ('MH', 'Marshall Islands'), ('MQ', 'Martinique'), ('MR', 'Mauritania'), ('MU', 'Mauritius'), ('YT', 'Mayotte'), ('MX', 'Mexico'), ('FM', 'Micronesia'), ('MD', 'Moldova, Republic of'), ('MC', 'Monaco'), ('MN', 'Mongolia'), ('MS', 'Monserrat'), ('MA', 'Morocco'), ('MZ', 'Mozambique'), ('MM', 'Myanmar'), ('NA', 'Nambia'), ('NR', 'Nauru'), ('NP', 'Nepal'), ('NL', 'Netherlands'), ('AN', 'Netherlands Antilles'), ('NT', 'Neutral Zone (no longer exists)'), ('NC', 'New Caledonia'), ('NZ', 'New Zealand'), ('NI', 'Nicaragua'), ('NE', 'Niger'), ('NG', 'Nigeria'), ('NU', 'Niue'), ('NF', 'Norfolk Island'), ('MP', 'Northern Mariana Islands'), ('NO', 'Norway'), ('OM', 'Oman'), ('PK', 'Pakistan'), ('PW', 'Palau'), ('PA', 'Panama'), ('PG', 'Papua New Guinea'), ('PY', 'Paraguay'), ('PE', 'Peru'), ('PH', 'Philippines'), ('PN', 'Pitcairn'), ('PL', 'Poland'), ('PT', 'Portugal'), ('PR', 'Puerto Rico'), ('QA', 'Qatar'), ('RE', 'RÃ©union'), ('RO', 'Romania'), ('RU', 'Russian Federation'), ('RW', 'Rwanda'), ('LC', 'Saint Lucia'), ('WS', 'Samoa'), ('SM', 'San Marino'), ('ST', 'Sao Tome &amp; Principe'), ('SA', 'Saudi Arabia'), ('SN', 'Senegal'), ('SC', 'Seychelles'), ('SL', 'Sierra Leone'), ('SG', 'Singapore'), ('SK', 'Slovakia'), ('SI', 'Slovenia'), ('SB', 'Solomon Islands'), ('SO', 'Somalia'), ('ZA', 'South Africa'), ('GS', 'South Georgia and the South Sandwich Islands'), ('ES', 'Spain'), ('LK', 'Sri Lanka'), ('SH', 'St. Helena'), ('KN', 'St. Kitts and Nevis'), ('PM', 'St. Pierre & Miquelon'), ('VC', 'St. Vincent & the Grenadines'), ('SD', 'Sudan'), ('SR', 'Suriname'), ('SJ', 'Svalbard & Jan Mayen Islands'), ('SZ', 'Swaziland'), ('SE', 'Sweden'), ('CH', 'Switzerland'), ('SY', 'Syrian Arab Republic'), ('TW', 'Taiwan, Province of China'), ('TJ', 'Tajikistan'), ('TZ', 'Tanzania, United Republic of'), ('TH', 'Thailand'), ('TG', 'Togo'), ('TK', 'Tokelau'), ('TO', 'Tonga'), ('TT', 'Trinidad &amp; Tobago'), ('TN', 'Tunisia'), ('TR', 'Turkey'), ('TM', 'Turkmenistan'), ('TC', 'Turks &amp; Caicos Islands'), ('TV', 'Tuvalu'), ('UG', 'Uganda'), ('UA', 'Ukraine'), ('SU', 'Union of Soviet Socialist Republics (no longer exi'), ('AE', 'United Arab Emirates'), ('GB', 'United Kingdom (Great Britain)'), ('UM', 'United States Minor Outlying Islands'), ('US', 'United States of America'), ('VI', 'United States Virgin Islands'), ('ZZ', 'Unknown or unspecified country'), ('UY', 'Uruguay'), ('UZ', 'Uzbekistan'), ('VU', 'Vanuatu'), ('VA', 'Vatican City State (Holy See)'), ('VE', 'Venezuela'), ('VN', 'Vietnam'), ('WF', 'Wallis & Futuna Islands'), ('EH', 'Western Sahara'), ('YE', 'Yemen'), ('YU', 'Yugoslavia'), ('ZR', 'Zaire'), ('ZM', 'Zambia'), ('ZW', 'Zimbabwe')], max_length=2, verbose_name='Departure country: ')),
                ('dep_date', models.DateField(verbose_name='Date of departure: ')),
                ('dest_airport', models.CharField(max_length=3, verbose_name='Destination airport (3-letter code): ')),
                ('dest_country', models.CharField(choices=[('AF', 'Afghanistan'), ('AL', 'Albania'), ('DZ', 'Algeria'), ('AS', 'American Samoa'), ('AD', 'Andorra'), ('AO', 'Angola'), ('AI', 'Anguilla'), ('AQ', 'Antarctica'), ('AG', 'Antigua & Barbuda'), ('AR', 'Argentina'), ('AM', 'Armenia'), ('AW', 'Aruba'), ('AU', 'Australia'), ('AT', 'Austria'), ('AZ', 'Azerbaijan'), ('BS', 'Bahama'), ('BH', 'Bahrain'), ('BD', 'Bangladesh'), ('BB', 'Barbados'), ('BY', 'Belarus'), ('BE', 'Belgium'), ('BZ', 'Belize'), ('BJ', 'Benin'), ('BM', 'Bermuda'), ('BT', 'Bhutan'), ('BO', 'Bolivia'), ('BA', 'Bosnia and Herzegovina'), ('BW', 'Botswana'), ('BV', 'Bouvet Island'), ('BR', 'Brazil'), ('IO', 'British Indian Ocean Territory'), ('VG', 'British Virgin Islands'), ('BN', 'Brunei Darussalam'), ('BG', 'Bulgaria'), ('BF', 'Burkina Faso'), ('BU', 'Burma (no longer exists)'), ('BI', 'Burundi'), ('KH', 'Cambodia'), ('CM', 'Cameroon'), ('CA', 'Canada'), ('CV', 'Cape Verde'), ('KY', 'Cayman Islands'), ('CF', 'Central African Republic'), ('TD', 'Chad'), ('CL', 'Chile'), ('CN', 'China'), ('CX', 'Christmas Island'), ('CC', 'Cocos (Keeling) Islands'), ('CO', 'Colombia'), ('KM', 'Comoros'), ('CG', 'Congo'), ('CK', 'Cook Islands'), ('CR', 'Costa Rica'), ('CI', "CÃ´te D'ivoire (Ivory Coast)"), ('HR', 'Croatia'), ('CU', 'Cuba'), ('CY', 'Cyprus'), ('CZ', 'Czech Republic'), ('CS', 'Czechoslovakia (no longer exists)'), ('YD', 'Democratic Yemen (no longer exists)'), ('DK', 'Denmark'), ('DJ', 'Djibouti'), ('DM', 'Dominica'), ('DO', 'Dominican Republic'), ('TP', 'East Timor'), ('EC', 'Ecuador'), ('EG', 'Egypt'), ('SV', 'El Salvador'), ('GQ', 'Equatorial Guinea'), ('ER', 'Eritrea'), ('EE', 'Estonia'), ('ET', 'Ethiopia'), ('FK', 'Falkland Islands (Malvinas)'), ('FO', 'Faroe Islands'), ('FJ', 'Fiji'), ('FI', 'Finland'), ('FR', 'France'), ('FX', 'France, Metropolitan'), ('GF', 'French Guiana'), ('PF', 'French Polynesia'), ('TF', 'French Southern Territories'), ('GA', 'Gabon'), ('GM', 'Gambia'), ('GE', 'Georgia'), ('DD', 'German Democratic Republic (no longer exists)'), ('DE', 'Germany'), ('GH', 'Ghana'), ('GI', 'Gibraltar'), ('GR', 'Greece'), ('GL', 'Greenland'), ('GD', 'Grenada'), ('GP', 'Guadeloupe'), ('GU', 'Guam'), ('GT', 'Guatemala'), ('GN', 'Guinea'), ('GW', 'Guinea-Bissau'), ('GY', 'Guyana'), ('HT', 'Haiti'), ('HM', 'Heard &amp; McDonald Islands'), ('HN', 'Honduras'), ('HK', 'Hong Kong'), ('HU', 'Hungary'), ('IS', 'Iceland'), ('IN', 'India'), ('ID', 'Indonesia'), ('IQ', 'Iraq'), ('IE', 'Ireland'), ('IR', 'Islamic Republic of Iran'), ('IL', 'Israel'), ('IT', 'Italy'), ('JM', 'Jamaica'), ('JP', 'Japan'), ('JO', 'Jordan'), ('KZ', 'Kazakhstan'), ('KE', 'Kenya'), ('KI', 'Kiribati'), ('KP', "Korea, Democratic People's Republic of"), ('KR', 'Korea, Republic of'), ('KW', 'Kuwait'), ('KG', 'Kyrgyzstan'), ('LA', "Lao People's Democratic Republic"), ('LV', 'Latvia'), ('LB', 'Lebanon'), ('LS', 'Lesotho'), ('LR', 'Liberia'), ('LY', 'Libyan Arab Jamahiriya'), ('LI', 'Liechtenstein'), ('LT', 'Lithuania'), ('LU', 'Luxembourg'), ('MO', 'Macau'), ('MG', 'Madagascar'), ('MW', 'Malawi'), ('MY', 'Malaysia'), ('MV', 'Maldives'), ('ML', 'Mali'), ('MT', 'Malta'), ('MH', 'Marshall Islands'), ('MQ', 'Martinique'), ('MR', 'Mauritania'), ('MU', 'Mauritius'), ('YT', 'Mayotte'), ('MX', 'Mexico'), ('FM', 'Micronesia'), ('MD', 'Moldova, Republic of'), ('MC', 'Monaco'), ('MN', 'Mongolia'), ('MS', 'Monserrat'), ('MA', 'Morocco'), ('MZ', 'Mozambique'), ('MM', 'Myanmar'), ('NA', 'Nambia'), ('NR', 'Nauru'), ('NP', 'Nepal'), ('NL', 'Netherlands'), ('AN', 'Netherlands Antilles'), ('NT', 'Neutral Zone (no longer exists)'), ('NC', 'New Caledonia'), ('NZ', 'New Zealand'), ('NI', 'Nicaragua'), ('NE', 'Niger'), ('NG', 'Nigeria'), ('NU', 'Niue'), ('NF', 'Norfolk Island'), ('MP', 'Northern Mariana Islands'), ('NO', 'Norway'), ('OM', 'Oman'), ('PK', 'Pakistan'), ('PW', 'Palau'), ('PA', 'Panama'), ('PG', 'Papua New Guinea'), ('PY', 'Paraguay'), ('PE', 'Peru'), ('PH', 'Philippines'), ('PN', 'Pitcairn'), ('PL', 'Poland'), ('PT', 'Portugal'), ('PR', 'Puerto Rico'), ('QA', 'Qatar'), ('RE', 'RÃ©union'), ('RO', 'Romania'), ('RU', 'Russian Federation'), ('RW', 'Rwanda'), ('LC', 'Saint Lucia'), ('WS', 'Samoa'), ('SM', 'San Marino'), ('ST', 'Sao Tome &amp; Principe'), ('SA', 'Saudi Arabia'), ('SN', 'Senegal'), ('SC', 'Seychelles'), ('SL', 'Sierra Leone'), ('SG', 'Singapore'), ('SK', 'Slovakia'), ('SI', 'Slovenia'), ('SB', 'Solomon Islands'), ('SO', 'Somalia'), ('ZA', 'South Africa'), ('GS', 'South Georgia and the South Sandwich Islands'), ('ES', 'Spain'), ('LK', 'Sri Lanka'), ('SH', 'St. Helena'), ('KN', 'St. Kitts and Nevis'), ('PM', 'St. Pierre & Miquelon'), ('VC', 'St. Vincent & the Grenadines'), ('SD', 'Sudan'), ('SR', 'Suriname'), ('SJ', 'Svalbard & Jan Mayen Islands'), ('SZ', 'Swaziland'), ('SE', 'Sweden'), ('CH', 'Switzerland'), ('SY', 'Syrian Arab Republic'), ('TW', 'Taiwan, Province of China'), ('TJ', 'Tajikistan'), ('TZ', 'Tanzania, United Republic of'), ('TH', 'Thailand'), ('TG', 'Togo'), ('TK', 'Tokelau'), ('TO', 'Tonga'), ('TT', 'Trinidad &amp; Tobago'), ('TN', 'Tunisia'), ('TR', 'Turkey'), ('TM', 'Turkmenistan'), ('TC', 'Turks &amp; Caicos Islands'), ('TV', 'Tuvalu'), ('UG', 'Uganda'), ('UA', 'Ukraine'), ('SU', 'Union of Soviet Socialist Republics (no longer exi'), ('AE', 'United Arab Emirates'), ('GB', 'United Kingdom (Great Britain)'), ('UM', 'United States Minor Outlying Islands'), ('US', 'United States of America'), ('VI', 'United States Virgin Islands'), ('ZZ', 'Unknown or unspecified country'), ('UY', 'Uruguay'), ('UZ', 'Uzbekistan'), ('VU', 'Vanuatu'), ('VA', 'Vatican City State (Holy See)'), ('VE', 'Venezuela'), ('VN', 'Vietnam'), ('WF', 'Wallis & Futuna Islands'), ('EH', 'Western Sahara'), ('YE', 'Yemen'), ('YU', 'Yugoslavia'), ('ZR', 'Zaire'), ('ZM', 'Zambia'), ('ZW', 'Zimbabwe')], max_length=2, verbose_name='Destination country: ')),
                ('dest_date', models.DateField(verbose_name='Date of arrival: ')),
                ('status', models.SmallIntegerField(choices=[(0, 'Still accepting offers'), (1, 'A deal is in progress'), (2, 'A deal is completed'), (3, 'The courier has departed'), (4, 'The courier has arrived'), (5, 'Cancelled')], default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, primary_key=True, serialize=False, to='auth.user')),
                ('profile', models.ImageField(upload_to='', verbose_name='Profile Picture: ')),
                ('name_f', models.CharField(max_length=32, verbose_name='First Name: ')),
                ('name_m', models.CharField(max_length=1, verbose_name='Middle Initial: ')),
                ('name_l', models.CharField(max_length=32, verbose_name='Last Name: ')),
                ('role', models.SmallIntegerField(choices=[(0, 'Sender'), (1, 'Courier')], verbose_name='Role: ')),
                ('phone_number', models.CharField(max_length=32, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+999999999'", regex='^\\+?1?\\d{9,15}$')], verbose_name='Cell Phone Number: ')),
                ('rating', models.FloatField(default=0)),
                ('referer', models.CharField(blank=True, max_length=10, verbose_name='Referral Code: ')),
                ('referee', models.CharField(default=mvpsite.models.create_ref, max_length=10)),
                ('address', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='profile_address', to='mvpsite.address', verbose_name='Home Address: ')),
            ],
        ),
        migrations.CreateModel(
            name='KYCAuth',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, primary_key=True, serialize=False, to='mvpsite.profile')),
                ('status', models.SmallIntegerField(choices=[(0, 'Pending'), (1, 'Completed Successfully'), (2, 'Failed'), (3, 'Raised to Supervisor')], default=0)),
                ('f_lic', models.ImageField(upload_to='', verbose_name="Front of driver's licence: ")),
                ('b_lic', models.ImageField(upload_to='', verbose_name="Back of driver's licence: ")),
                ('mail_item', models.ImageField(upload_to='', verbose_name='Piece of mail with your name and address: ')),
            ],
        ),
        migrations.CreateModel(
            name='PackageAd',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('desc', models.TextField(verbose_name="Description - Include what's in the package (hazards, fragile items): ")),
                ('package_type', models.SmallIntegerField(choices=[(0, 'In luggage'), (1, 'Separate bag'), (2, 'Oversize')], verbose_name='Type of package: ')),
                ('package_weight', models.FloatField(verbose_name='Approximate weight (lb): ')),
                ('package_length', models.FloatField(verbose_name='Length (in): ')),
                ('package_width', models.FloatField(verbose_name='Width (in): ')),
                ('package_depth', models.FloatField(verbose_name='Depth (in): ')),
                ('package_image', models.ImageField(upload_to='', verbose_name='Photo of the package: ')),
                ('package_price_max', models.FloatField(verbose_name='Price maximum (USD): ')),
                ('sender_mode', models.SmallIntegerField(choices=[(0, 'In Person'), (1, 'Delivery Service')], verbose_name='Pickup mode: ')),
                ('receiver_mode', models.SmallIntegerField(choices=[(0, 'In Person'), (1, 'Delivery Service')], verbose_name='Drop-off mode: ')),
                ('receiver_number', models.CharField(max_length=32, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+999999999'", regex='^\\+?1?\\d{9,15}$')], verbose_name="Receiver's phone number: ")),
                ('status', models.SmallIntegerField(choices=[(0, 'Still accepting offers'), (1, 'A deal is in progress'), (2, 'A deal is completed'), (3, 'The package has been dropped off'), (4, 'The package is with the courier'), (5, 'The courier has delivered the package'), (6, 'The package has been received'), (7, 'Cancelled')], default=0)),
                ('courier', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.PROTECT, related_name='packagead_courier', to='mvpsite.courierad')),
                ('receiver_address', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='packagead_receive_a', to='mvpsite.address', verbose_name="Receiver's address NOT delivery service address: ")),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='packagead_sender', to='mvpsite.profile')),
                ('sender_address', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='packagead_send_a', to='mvpsite.address', verbose_name='Pickup address OR delivery service address: ')),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('regarding_code', models.SmallIntegerField(choices=[(1, 'Courier Ad'), (2, 'Package Ad'), (3, 'Other')])),
                ('regarding_uuid', models.UUIDField()),
                ('time', models.DateTimeField(auto_now=True)),
                ('seen', models.BooleanField()),
                ('receiver', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='message_receive', to='mvpsite.profile')),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='message_sender', to='mvpsite.profile')),
            ],
        ),
        migrations.AddField(
            model_name='courierad',
            name='courier',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='courierad_courier', to='mvpsite.profile'),
        ),
    ]
