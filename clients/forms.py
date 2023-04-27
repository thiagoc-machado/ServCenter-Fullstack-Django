from django.forms import ModelForm
from .models import client
from django.shortcuts import render


class FormClient(ModelForm):
    class Meta:
        model = client
        exclude = ['-ativo']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields:

            if field == "ativo":
                self.fields['ativo'].widget.attrs.update(
                    {'class': 'form-check'})

            else:
                self.fields[field].widget.attrs.update(
                    {'class': 'form-control'})

        def edit_record(request, cod_cli):
            record = client.objects.get(id=cod_cli)
            form = client(instance=record)
            return render(request, 'edit_client.html', {'form': form, 'record_id': cod_cli})
