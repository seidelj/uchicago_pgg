# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import save_the_change.mixins
import otree.db.models


class Migration(migrations.Migration):

    dependencies = [
        ('otree', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('_is_missing_players', otree.db.models.BooleanField(default=False, choices=[(True, 'Yes'), (False, 'No')])),
                ('id_in_subsession', otree.db.models.PositiveIntegerField(null=True)),
                ('session', otree.db.models.ForeignKey(related_name='quizes_group', to='otree.Session')),
            ],
            options={
                'ordering': ['pk'],
                'abstract': False,
            },
            bases=(save_the_change.mixins.SaveTheChange, models.Model),
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('_index_in_game_pages', otree.db.models.PositiveIntegerField(default=0, null=True)),
                ('round_number', otree.db.models.PositiveIntegerField(null=True)),
                ('id_in_group', otree.db.models.PositiveIntegerField(null=True)),
                ('payoff', otree.db.models.CurrencyField(null=True, max_digits=12)),
                ('label', otree.db.models.CharField(max_length=500, null=True)),
                ('q_first_q1', otree.db.models.CharField(max_length=500, null=True, choices=[(b'True', b'True'), (b'False', b'False')])),
                ('q_first_q2', otree.db.models.CharField(max_length=500, null=True, choices=[(b'True', b'True'), (b'False', b'False')])),
                ('q_first_q3', otree.db.models.CharField(max_length=500, null=True, choices=[(b'True', b'True'), (b'False', b'False')])),
                ('q_first_q4', otree.db.models.CharField(max_length=500, null=True, choices=[(b'True', b'True'), (b'False', b'False')])),
                ('q_first_q5', otree.db.models.CharField(max_length=500, null=True, choices=[(b'True', b'True'), (b'False', b'False')])),
                ('q_first_q6', otree.db.models.CharField(max_length=500, null=True, choices=[(b'True', b'True'), (b'False', b'False')])),
                ('private_2_q1', otree.db.models.CharField(max_length=500, null=True, choices=[(b'True', b'True'), (b'False', b'False')])),
                ('private_2_q2', otree.db.models.CharField(max_length=500, null=True, choices=[(b'True', b'True'), (b'False', b'False')])),
                ('private_2_q3', otree.db.models.CharField(max_length=500, null=True, choices=[(b'True', b'True'), (b'False', b'False')])),
                ('private_2_q4', otree.db.models.CharField(max_length=500, null=True, choices=[(b'1', b'0.45, 0.55, 0.65'), (b'2', b'0.25, 0.35, 0.45'), (b'3', b'0.35, 0.45, 0.55')])),
                ('private_3_q1', otree.db.models.CharField(max_length=500, null=True, choices=[(b'True', b'True'), (b'False', b'False')])),
                ('private_3_q2', otree.db.models.CharField(max_length=500, null=True, choices=[(b'1', b'0.95, 1.05, 1.15'), (b'2', b'0.85, 0.95, 1.05'), (b'3', b'0.75, 0.85, 0.95')])),
                ('exact_2_q1', otree.db.models.CharField(max_length=500, null=True, choices=[(b'True', b'True'), (b'False', b'False')])),
                ('exact_3_q1', otree.db.models.CharField(max_length=500, null=True, choices=[(b'True', b'True'), (b'False', b'False')])),
                ('public_2_q1', otree.db.models.CharField(max_length=500, null=True, choices=[(b'True', b'True'), (b'False', b'False')])),
                ('public_2_q2', otree.db.models.CharField(max_length=500, null=True, choices=[(b'True', b'True'), (b'False', b'False')])),
                ('public_2_q3', otree.db.models.CharField(max_length=500, null=True, choices=[(b'True', b'True'), (b'False', b'False')])),
                ('public_2_q4', otree.db.models.CharField(max_length=500, null=True, choices=[(b'1', b'1.05, 1.15, 1.25'), (b'2', b'0.95, 1.05'), (b'3', b'1.05')])),
                ('public_3_q1', otree.db.models.CharField(max_length=500, null=True, choices=[(b'True', b'True'), (b'False', b'False')])),
                ('public_3_q2', otree.db.models.CharField(max_length=500, null=True, choices=[(b'True', b'True'), (b'False', b'False')])),
                ('public_3_q3', otree.db.models.CharField(max_length=500, null=True, choices=[(b'1', b'0.95, 1.05, 1.15'), (b'2', b'1.05, 1.15'), (b'3', b'1.05, 1.15, 1.25')])),
                ('private_wide_2_q1', otree.db.models.CharField(max_length=500, null=True, choices=[(b'True', b'True'), (b'False', b'False')])),
                ('private_wide_2_q2', otree.db.models.CharField(max_length=500, null=True, choices=[(b'True', b'True'), (b'False', b'False')])),
                ('private_wide_2_q3', otree.db.models.CharField(max_length=500, null=True, choices=[(b'True', b'True'), (b'False', b'False')])),
                ('private_wide_2_q4', otree.db.models.CharField(max_length=500, null=True, choices=[(b'1', b'0.45, 0.55, 0.65'), (b'2', b'0.25, 0.35, 0.45'), (b'3', b'0.35, 0.45, 0.55')])),
                ('private_wide_3_q1', otree.db.models.CharField(max_length=500, null=True, choices=[(b'True', b'True'), (b'False', b'False')])),
                ('private_wide_3_q2', otree.db.models.CharField(max_length=500, null=True, choices=[(b'1', b'0.95, 1.05, 1.15'), (b'2', b'0.85, 0.95, 1.05'), (b'3', b'0.75, 0.85, 0.95')])),
                ('public_wide_2_q1', otree.db.models.CharField(max_length=500, null=True, choices=[(b'True', b'True'), (b'False', b'False')])),
                ('public_wide_2_q2', otree.db.models.CharField(max_length=500, null=True, choices=[(b'True', b'True'), (b'False', b'False')])),
                ('public_wide_2_q3', otree.db.models.CharField(max_length=500, null=True, choices=[(b'True', b'True'), (b'False', b'False')])),
                ('public_wide_2_q4', otree.db.models.CharField(max_length=500, null=True, choices=[(b'1', b'1.05, 1.15, 1.25'), (b'2', b'0.95, 1.05'), (b'3', b'1.05')])),
                ('public_wide_3_q1', otree.db.models.CharField(max_length=500, null=True, choices=[(b'True', b'True'), (b'False', b'False')])),
                ('public_wide_3_q2', otree.db.models.CharField(max_length=500, null=True, choices=[(b'True', b'True'), (b'False', b'False')])),
                ('public_wide_3_q3', otree.db.models.CharField(max_length=500, null=True, choices=[(b'1', b'0.95, 1.05, 1.15'), (b'2', b'1.05, 1.15'), (b'3', b'1.05, 1.15, 1.25')])),
                ('group', otree.db.models.ForeignKey(to='quizes.Group', null=True)),
                ('participant', otree.db.models.ForeignKey(related_name='quizes_player', to='otree.Participant')),
                ('session', otree.db.models.ForeignKey(related_name='quizes_player', to='otree.Session')),
            ],
            options={
                'ordering': ['pk'],
                'abstract': False,
            },
            bases=(save_the_change.mixins.SaveTheChange, models.Model),
        ),
        migrations.CreateModel(
            name='Subsession',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', otree.db.models.RandomCharField(max_length=8, blank=True)),
                ('_index_in_subsessions', otree.db.models.PositiveIntegerField(null=True)),
                ('round_number', otree.db.models.PositiveIntegerField(null=True)),
                ('session', otree.db.models.ForeignKey(related_name='quizes_subsession', to='otree.Session', null=True)),
            ],
            options={
                'ordering': ['pk'],
                'abstract': False,
            },
            bases=(save_the_change.mixins.SaveTheChange, models.Model),
        ),
        migrations.AddField(
            model_name='player',
            name='subsession',
            field=otree.db.models.ForeignKey(to='quizes.Subsession'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='group',
            name='subsession',
            field=otree.db.models.ForeignKey(to='quizes.Subsession'),
            preserve_default=True,
        ),
    ]
