# Generated by Django 4.1 on 2022-09-03 09:39

import chords.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Chord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('root', chords.fields.NoteField(choices=[(0, 'C'), (1, 'Db'), (2, 'D'), (3, 'Eb'), (4, 'E'), (5, 'F'), (6, 'Gb'), (7, 'G'), (8, 'Ab'), (9, 'A'), (10, 'Bb'), (11, 'B')])),
                ('notes', chords.fields.NotesField(choices=[(0, 'C'), (1, 'Db'), (2, 'D'), (3, 'Eb'), (4, 'E'), (5, 'F'), (6, 'Gb'), (7, 'G'), (8, 'Ab'), (9, 'A'), (10, 'Bb'), (11, 'B')], default=set(), editable=False, max_length=12)),
            ],
        ),
        migrations.CreateModel(
            name='ChordType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, unique=True)),
                ('base', models.CharField(choices=[('DIM', 'Diminished'), ('MIN', 'Minor'), ('MAJ', 'Major'), ('AUG', 'Augmented')], max_length=30)),
                ('seventh', chords.fields.IntervalField(blank=True, choices=[(0, 'P1'), (1, 'm2'), (2, 'M2'), (3, 'm3'), (4, 'M3'), (5, 'P4'), (6, 'dim5'), (7, 'P5'), (8, 'm6'), (9, 'M6'), (10, 'm7'), (11, 'M7'), (12, '(8)'), (13, 'm9'), (14, 'M9'), (15, 'm10'), (16, 'M10'), (17, 'P11'), (18, 'aug11'), (19, 'P12'), (20, 'm13'), (21, 'M13'), (22, 'aug13')], null=True)),
                ('extensions', chords.fields.IntervalsField(blank=True, choices=[(0, 'P1'), (1, 'm2'), (2, 'M2'), (3, 'm3'), (4, 'M3'), (5, 'P4'), (6, 'dim5'), (7, 'P5'), (8, 'm6'), (9, 'M6'), (10, 'm7'), (11, 'M7'), (12, '(8)'), (13, 'm9'), (14, 'M9'), (15, 'm10'), (16, 'M10'), (17, 'P11'), (18, 'aug11'), (19, 'P12'), (20, 'm13'), (21, 'M13'), (22, 'aug13')], max_length=12)),
            ],
        ),
        migrations.CreateModel(
            name='Scale',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('notes', models.JSONField(default=[0, 2, 4, 5, 7, 9, 11], verbose_name='Notes')),
            ],
        ),
        migrations.CreateModel(
            name='Relation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('transposition', chords.fields.IntervalField()),
                ('chord_type_a', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ascending_relations', to='chords.chordtype')),
                ('chord_type_b', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='descending_relations', to='chords.chordtype')),
            ],
        ),
        migrations.CreateModel(
            name='Pitch',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('note', chords.fields.NoteField(choices=[(0, 'C'), (1, 'Db'), (2, 'D'), (3, 'Eb'), (4, 'E'), (5, 'F'), (6, 'Gb'), (7, 'G'), (8, 'Ab'), (9, 'A'), (10, 'Bb'), (11, 'B')])),
                ('octave', models.IntegerField()),
                ('audio', models.FileField(blank=True, null=True, upload_to='audio/')),
            ],
            options={
                'unique_together': {('note', 'octave')},
            },
        ),
        migrations.CreateModel(
            name='ChordVoicing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('chord', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='voicings', to='chords.chord')),
                ('pitches', models.ManyToManyField(to='chords.pitch')),
            ],
        ),
        migrations.AddField(
            model_name='chord',
            name='chord_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='chords.chordtype'),
        ),
        migrations.AlterUniqueTogether(
            name='chord',
            unique_together={('root', 'chord_type')},
        ),
    ]
