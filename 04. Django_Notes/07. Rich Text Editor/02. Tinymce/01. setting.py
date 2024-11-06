pip install django-tinymce

https://django-tinymce.readthedocs.io/en/latest/installation.html



#Download JS files:
https://download.tiny.cloud/tinymce/community/tinymce_6.8.2.zip

static / tinymcejs / files

'''
/* Hiding Tinymce Credit*/
.tox-promotion, .tox-statusbar__branding{
  display: none!important;
}
.tox .tox-promotion{
    display: none!important;
}
.tox .tox-statusbar__right-container{
    display: none!important;
}
'''


# Appp
INSTALLED_APPS = (
    ...
    'tinymce',
    ...
)

# Tinymc..................
TINYMCE_JS_URL = os.path.join(MEDIA_URL, "tinymce/tinymce.min.js")
TINYMCE_COMPRESSOR = False

TINYMCE_DEFAULT_CONFIG = {
    "height": "320px",
    "width": "960px",
    "menubar": "file edit view insert format tools table help",
    "plugins": "advlist autolink lists link image charmap print preview anchor searchreplace visualblocks code "
    "fullscreen insertdatetime media table paste code help wordcount spellchecker",
    "toolbar": "undo redo | bold italic underline strikethrough | fontselect fontsizeselect formatselect | alignleft "
    "aligncenter alignright alignjustify | outdent indent |  numlist bullist checklist | forecolor "
    "backcolor casechange permanentpen formatpainter removeformat | pagebreak | charmap emoticons | "
    "fullscreen  preview save print | insertfile image media pageembed template link anchor codesample | "
    "a11ycheck ltr rtl | showcomments addcomment code",
    "custom_undo_redo_levels": 10,
    "language": "es_ES",  # To force a specific language instead of the Django current language.
}
TINYMCE_SPELLCHECKER = True
TINYMCE_COMPRESSOR = True
TINYMCE_EXTRA_MEDIA = {
    'css': {
        'all': [
            ...
        ],
    },
    'js': [
        ...
    ],
}
