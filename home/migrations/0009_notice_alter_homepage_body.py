import json

import home.models

from django.core.serializers.json import DjangoJSONEncoder
from django.db import migrations, models

import wagtail.blocks
import wagtail.fields


def convert_to_streamfield(apps, schema_editor):
    HomePage = apps.get_model("home", "HomePage")
    for page in HomePage.objects.all():
        page.body = json.dumps(
            [{"type": "paragraph", "value": page.body}],
            cls=DjangoJSONEncoder
        )
        page.save()


def convert_to_richtext(apps, schema_editor):
    HomePage = apps.get_model("home", "HomePage")
    for page in HomePage.objects.all():
        if page.body:
            stream = json.loads(page.body)
            page.body = "".join([
                child["value"] for child in stream
                if child["type"] == "paragraph"
            ])
            page.save()


class Migration(migrations.Migration):

    dependencies = [
        # leave the dependency line from the generated migration intact!
        ('home', '0008_contactuspage_contactfield'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('heading', models.CharField(max_length=255)),
                ('message', wagtail.fields.RichTextField()),
            ],
        ),
        migrations.RunPython(
            convert_to_streamfield,
            convert_to_richtext,
        ),

        # leave the generated AlterField intact!
        migrations.AlterField(
            model_name="HomePage",
            name="body",
            field=wagtail.fields.StreamField([('heading', 0), ('paragraph', 1), ('image', 2), ('product_table', 5), ('notice', 6)], block_lookup={0: ('wagtail.blocks.CharBlock', (), {'form_classname': 'title'}), 1: ('wagtail.blocks.RichTextBlock', (), {}), 2: ('wagtail.images.blocks.ImageChooserBlock', (), {}), 3: ('wagtail.blocks.CharBlock', (), {}), 4: ('wagtail.blocks.ListBlock', (home.models.ProductBlock,), {}), 5: ('wagtail.blocks.StructBlock', [[('heading', 3), ('description', 1), ('products', 4)]], {}), 6: ('wagtail.snippets.blocks.SnippetChooserBlock', (home.models.Notice,), {})}),
        ),
    ]