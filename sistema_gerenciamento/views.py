from django.contrib.auth.hashers import make_password
from django.core.exceptions import PermissionDenied
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.shortcuts import render, redirect, get_object_or_404
from django.http.response import HttpResponse, Http404, FileResponse
from django.contrib.auth import authenticate, logout
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required, permission_required
from .models import Veiculo, Manutencao, Checklist, Motorista, Rota,Combustivel, Demanda, Viagem
from .forms import (VeiculoForm, ManutencaoForm, ChecklistForm, CadastroForm, LoginForm, MotoristasForm,
                    CombustivelForm, RotaForm, DemandaForm, ViagemForm)


# Create your views here.
def cadastro(request):
    if request.method == "GET":
        form = CadastroForm()
        return render(request, 'cadastro.html', {'form': form})

    else:
        form = CadastroForm(request.POST)
        if form.is_valid():
            form.instance.password = make_password(form.cleaned_data['password1'])
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'cadastro.html', {'form': form})


# user_login view
def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)

        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Nome de usuário ou senha incorretos.')

    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})

# user_logout view
@login_required(login_url="/auth/user_login/")
def user_logout(request):
    logout(request)
    messages.success(request, 'Você foi desconectado com sucesso.')
    return redirect('user_login')


@login_required(login_url="/auth/user_login/")
def home(request):
    user = request.user
    return render(request, 'home.html', {'user': user})


@login_required(login_url="/auth/user_login/")
def veiculos(request):
    if request.method == 'GET':
        veiculos_list = Veiculo.objects.all()

        ordenacao = request.GET.get('ordenacao', '')
        if ordenacao == 'asc':
            veiculos_list = veiculos_list.order_by('data_cadastro')
        elif ordenacao == 'desc':
            veiculos_list = veiculos_list.order_by('-data_cadastro')

        user_permissions = {
            'view_cadastrar_veiculos': request.user.has_perm('sistema_gerenciamento.view_cadastrar_veiculos'),
            'view_editar_veiculo': request.user.has_perm('sistema_gerenciamento.view_editar_veiculo'),
            'view_deletar_veiculo': request.user.has_perm('sistema_gerenciamento.view_deletar_veiculo'),
        }
        return render(request, 'veiculo/veiculos.html', {'veiculos_list': veiculos_list, 'user_permissions': user_permissions})


@login_required(login_url="/auth/user_login/")
@permission_required('sistema_gerenciamento.view_cadastrar_veiculos', raise_exception=True)
def cadastrar_veiculos(request):
    if request.method == 'GET':
        form = VeiculoForm()
        return render(request, 'veiculo/cadastrar_veiculos.html', {'form':form})
    else:
        form = VeiculoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('veiculos')
        else:
            return render(request, 'veiculo/cadastrar_veiculos.html', {'form':form})


@login_required(login_url="/auth/user_login/")
@permission_required('sistema_gerenciamento.view_editar_veiculo', raise_exception=True)
def editar_veiculo(request, veiculo_id):
    veiculo = get_object_or_404(Veiculo, pk=veiculo_id)

    if request.method == 'POST':
        form = VeiculoForm(request.POST, instance=veiculo)
        if form.is_valid():
            form.save()
            return redirect('veiculos')
    else:
        form = VeiculoForm(instance=veiculo)

    return  render(request, 'veiculo/editar_veiculo.html', {'form':form, 'veiculo':veiculo})


@login_required(login_url="/auth/user_login/")
@permission_required('sistema_gerenciamento.view_deletar_veiculos', raise_exception=True)
def deletar_veiculo(request, veiculo_id):
    veiculo = get_object_or_404(Veiculo, id=veiculo_id)
    veiculo.delete()
    return redirect('veiculos')


@login_required(login_url="/auth/user_login/")
def manutencao(request):
    if request.method == 'GET':
        manutencoes_list = Manutencao.objects.all()

        ordenacao = request.GET.get('ordenacao', '')
        if ordenacao == 'asc':
            manutencoes_list = manutencoes_list.order_by('data')
        elif ordenacao == 'desc':
            manutencoes_list = manutencoes_list.order_by('-data')

        user_permissions = {
            'view_cadastrar_manutencao': request.user.has_perm('sistema_gerenciamento.view_cadastrar_manutencao'),
            'view_editar_manutencao': request.user.has_perm('sistema_gerenciamento.view_editar_manutencao'),
            'view_deletar_manutencao': request.user.has_perm('sistema_gerenciamento.view_deletar_manutencao'),
        }

        return render(request, 'veiculo/manutencao.html', {'manutencoes_list': manutencoes_list, 'user_permissions': user_permissions})


@login_required(login_url="/auth/user_login/")
@permission_required('sistema_gerenciamento.view_cadastrar_manutencao', raise_exception=True)
def cadastrar_manutencao(request):
    if request.method == 'GET':
        form = ManutencaoForm()
        return render(request, 'veiculo/cadastrar_manutencao.html', {'form': form})
    else:
        form = ManutencaoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('manutencao')

    return render(request, 'veiculo/cadastrar_manutencao.html', {'form': form})


@login_required(login_url="/auth/user_login/")
def view_comprovante(request, manutencao_id):
    manutencao = Manutencao.objects.get(id=manutencao_id)
    image_data = open(manutencao.comprovante_manutencao.path, "rb").read()
    return HttpResponse(image_data, content_type="image/png")


@login_required(login_url="/auth/user_login/")
def manutencoes_veiculo(request, veiculo_id):
    veiculo = Veiculo.objects.get(pk=veiculo_id)
    manutencoes = Manutencao.objects.filter(veiculo=veiculo)

    ordenacao = request.GET.get('ordenacao', '')
    if ordenacao == 'asc':
        manutencoes = manutencoes.order_by('data')
    elif ordenacao == 'desc':
        manutencoes = manutencoes.order_by('-data')

    return render(request, 'veiculo/manutencoes_veiculo.html', {'veiculo': veiculo, 'manutencoes': manutencoes})


@login_required(login_url="/auth/user_login/")
@permission_required('sistema_gerenciamento.view_editar_manutencao', raise_exception=True)
def editar_manutencao(request, manutencao_id):
    manutencao = get_object_or_404(Manutencao, pk=manutencao_id)

    if request.method == 'POST':
        form = ManutencaoForm(request.POST, request.FILES, instance=manutencao)
        if form.is_valid():
            print('validado')
            novo_comprovante = form.cleaned_data.get('comprovante_manutencao')
            if isinstance(novo_comprovante, InMemoryUploadedFile):
                manutencao.comprovante_manutencao = novo_comprovante
                print('Manutenção salva com sucessoo')
            form.save()
            return redirect('manutencao')  # Redireciona apenas após a submissão bem-sucedida
    else:
        form = ManutencaoForm(instance=manutencao)

    return render(request, 'veiculo/editar_manutencao.html', {'form':form, 'manutencao':manutencao})


@login_required(login_url="/auth/user_login/")
@permission_required('sistema_gerenciamento.view_deletar_manutencao', raise_exception=True)
def deletar_manutencao(request, manutencao_id):
    manutencao = get_object_or_404(Manutencao, id=manutencao_id)
    manutencao.delete()
    return redirect('manutencao')


@login_required(login_url="/auth/user_login/")
def checklists(request):
    if request.method == 'GET':
        checklist_list = Checklist.objects.all()

        ordenacao = request.GET.get('ordenacao', '')
        if ordenacao == 'asc':
            checklist_list = checklist_list.order_by('data')
        elif ordenacao == 'desc':
            checklist_list = checklist_list.order_by('-data')

        user_permissions = {
            'view_cadastrar_checklist': request.user.has_perm('sistema_gerenciamento.view_cadastrar_checklist'),
            'view_editar_checklist': request.user.has_perm('sistema_gerenciamento.view_editar_checklist'),
            'view_deletar_checklist': request.user.has_perm('sistema_gerenciamento.view_deletar_checklist'),
        }

        return render(request, 'veiculo/checklists.html', {'checklist_list': checklist_list, 'user_permissions': user_permissions})


@login_required(login_url="/auth/user_login/")
@permission_required('sistema_gerenciamento.view_cadastrar_checklist', raise_exception=True)
def cadastrar_checklist(request):
    if request.method == 'GET':
        form = ChecklistForm
        return render(request, 'veiculo/cadastrar_checklist.html', {'form': form})
    else:
        form = ChecklistForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('checklists')

    return render(request, 'veiculo/cadastrar_checklist.html', {'form': form})


@login_required(login_url="/auth/user_login/")
def view_comprovante_checklist(request, checklist_id):
    checklist = Checklist.objects.get(id=checklist_id)
    image_data = open(checklist.comprovante_checklist.path, "rb").read()
    return HttpResponse(image_data, content_type="image/png")


@login_required(login_url="/auth/user_login/")
@permission_required('sistema_gerenciamento.view_editar_checklist', raise_exception=True)
def editar_checklist(request, checklist_id):
    checklist = get_object_or_404(Checklist, pk=checklist_id)

    if request.method == 'POST':
        form = ChecklistForm(request.POST, request.FILES, instance=checklist)
        if form.is_valid():
            novo_comprovante = form.cleaned_data.get('comprovante_checklist')
            if isinstance(novo_comprovante, InMemoryUploadedFile):
                checklist.comprovante_checklist = novo_comprovante
            form.save()
            return redirect('checklists')  # Redireciona apenas após a submissão bem-sucedida
    else:
        form = ChecklistForm(instance=checklist)

    return render(request, 'veiculo/editar_checklist.html', {'form': form, 'checklist':checklist})


@login_required(login_url="/auth/user_login/")
@permission_required('sistema_gerenciamento.view_deletar_checklist', raise_exception=True)
def deletar_checklist(request, checklist_id):
    checklist = get_object_or_404(Checklist, id=checklist_id)
    checklist.delete()
    return redirect('checklists')


@login_required(login_url="/auth/user_login/")
def motoristas(request):
    if request.method == 'GET':
        motoristas_list = Motorista.objects.all()

        ordenacao = request.GET.get('ordenacao', '')
        if ordenacao == 'asc':
            motoristas_list = motoristas_list.order_by('data_cadastro')
        elif ordenacao == 'desc':
            motoristas_list = motoristas_list.order_by('-data_cadastro')

        user_permissions = {
            'view_cadastrar_motorista': request.user.has_perm('sistema_gerenciamento.view_cadastrar_motorista'),
            'view_editar_motorista': request.user.has_perm('sistema_gerenciamento.view_editar_motorista'),
            'view_deletar_motorista': request.user.has_perm('sistema_gerenciamento.view_deletar_motorista'),
        }

        return render(request, 'motoristas/motoristas.html', {'motoristas_list': motoristas_list, 'user_permissions': user_permissions})


@login_required(login_url="/auth/user_login/")
@permission_required('sistema_gerenciamento.view_cadastrar_motorista', raise_exception=True)
def cadastrar_motorista(request):
    if request.method == 'GET':
        form = MotoristasForm
        return render(request, 'motoristas/cadastrar_motorista.html', {'form':form})
    else:
        form = MotoristasForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('motoristas')
        else:
            return render(request, 'motoristas/cadastrar_motorista.html', {'form': form})


@login_required(login_url="/auth/user_login/")
def visualizar_documentos(request, motorista_id):
    motorista = get_object_or_404(Motorista, pk=motorista_id)

    if not motorista.documentos:
        raise Http404("Documento não encontrado")

    response = FileResponse(motorista.documentos.open('rb'))
    return response


@login_required(login_url="/auth/user_login/")
@permission_required('sistema_gerenciamento.view_editar_motorista', raise_exception=True)
def editar_motorista(request, motorista_id):
    motorista = get_object_or_404(Motorista, pk=motorista_id)

    if request.method == 'POST':
        form = MotoristasForm(request.POST, request.FILES, instance=motorista)
        if form.is_valid():
            form.save()
            return redirect('motoristas')
    else:
        form = MotoristasForm(instance=motorista)

    return render(request, 'motoristas/editar_motorista.html', {'form': form, 'motorista': motorista})


@login_required(login_url="/auth/user_login/")
@permission_required('sistema_gerenciamento.view_deletar_motorista', raise_exception=True)
def deletar_motorista(request, motorista_id):
    motorista = get_object_or_404(Motorista, pk=motorista_id)
    motorista.delete()
    return redirect('motoristas')


@login_required(login_url="/auth/user_login/")
def rotas(request):
    if request.method == 'GET':
        rotas_list = Rota.objects.all()

        user_permissions = {
            'view_cadastrar_rota': request.user.has_perm('sistema_gerenciamento.view_cadastrar_rota'),
            'view_editar_rota': request.user.has_perm('sistema_gerenciamento.view_editar_rota'),
            'view_deletar_rota': request.user.has_perm('sistema_gerenciamento.view_deletar_rota'),
        }

        return render(request, 'rotas/rotas.html', {'rotas_list':rotas_list, 'user_permissions': user_permissions})


@login_required(login_url="/auth/user_login/")
@permission_required('sistema_gerenciamento.view_cadastrar_rota',raise_exception=True)
def cadastrar_rota(request):
    if request.method == 'GET':
        form = RotaForm
        return render(request, 'rotas/cadastrar_rota.html', {'form':form})
    else:
        form = RotaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('rotas')
        else:
            return render(request, 'rotas/cadastrar_rota.html', {'form': form})


@login_required(login_url="/auth/user_login/")
@permission_required('sistema_gerenciamento.view_editar_rota',raise_exception=True)
def editar_rota(request, rota_id):
    rota = get_object_or_404(Rota, pk=rota_id)
    motoristas = Motorista.objects.all()
    veiculos = Veiculo.objects.all()

    if request.method == 'POST':
        form = RotaForm(request.POST, instance=rota)
        if form.is_valid():
            form.save()
            return redirect('rotas')
    else:
        form = RotaForm(instance=rota)

    return render(request, 'rotas/editar_rota.html', {'form': form, 'rota': rota, 'motoristas':motoristas, 'veiculos':veiculos})


@login_required(login_url="/auth/user_login/")
@permission_required('sistema_gerenciamento.view_deletar_rota',raise_exception=True)
def deletar_rota(request, rota_id):
    rota = get_object_or_404(Rota, pk=rota_id)
    rota.delete()
    return redirect('rotas')


@login_required(login_url="/auth/user_login/")
def combustivel(request):
    if request.method == 'GET':
        abastecimentos_list = Combustivel.objects.all()

        ordenacao = request.GET.get('ordenacao', '')
        if ordenacao == 'asc':
            abastecimentos_list = abastecimentos_list.order_by('data_cadastro')
        elif ordenacao == 'desc':
            abastecimentos_list = abastecimentos_list.order_by('-data_cadastro')

        user_permissions = {
            'view_cadastrar_abastecimento': request.user.has_perm('sistema_gerenciamento.view_cadastrar_abastecimento'),
            'view_editar_abastecimento': request.user.has_perm('sistema_gerenciamento.view_editar_abastecimento'),
            'view_deletar_abastecimento': request.user.has_perm('sistema_gerenciamento.view_deletar_abastecimento'),
        }

        return render(request, 'combustivel/combustivel.html', {'abastecimentos_list': abastecimentos_list, 'user_permissions': user_permissions})


@login_required(login_url="/auth/user_login/")
@permission_required('sistema_gerenciamento.view_cadastrar_abastecimento',raise_exception=True)
def cadastrar_abastecimento(request):
    if request.method == 'GET':
        form = CombustivelForm
        return render(request, 'combustivel/cadastrar_abastecimento.html', {'form':form})
    else:
        form = CombustivelForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('combustivel')
        else:
            return render(request, 'combustivel/cadastrar_abastecimento.html', {'form': form})


@login_required(login_url="/auth/user_login/")
def view_comprovante_abastecimento(request, abastecimento_id):
    abastecimento = Combustivel.objects.get(id=abastecimento_id)
    image_data = open(abastecimento.comprovante_abastecimento.path, "rb").read()
    return HttpResponse(image_data, content_type="image/png")


@login_required(login_url="/auth/user_login/")
@permission_required('sistema_gerenciamento.view_editar_abastecimento',raise_exception=True)
def editar_abastecimento(request, abastecimento_id):
    abastecimento = get_object_or_404(Combustivel, pk=abastecimento_id)

    if request.method == 'POST':
        form = CombustivelForm(request.POST, request.FILES, instance=abastecimento)
        if form.is_valid():
            novo_comprovante = form.cleaned_data.get('comprovante_abastecimento')
            if isinstance(novo_comprovante, InMemoryUploadedFile):
                abastecimento.comprovante_abastecimento = novo_comprovante
            form.save()
            return redirect('combustivel')  # Redireciona apenas após a submissão bem-sucedida
    else:
        form = CombustivelForm(instance=abastecimento)

    return render(request, 'combustivel/editar_abastecimento.html', {'form': form, 'abastecimento': abastecimento})


@login_required(login_url="/auth/user_login/")
@permission_required('sistema_gerenciamento.view_deletar_abastecimento',raise_exception=True)
def deletar_abastecimento(request, abastecimento_id):
    abastecimento = get_object_or_404(Combustivel, pk=abastecimento_id)
    abastecimento.delete()
    return redirect('combustivel')


@login_required(login_url="/auth/user_login/")
def demandas(request):
    if request.method == 'GET':
        demandas_list = Demanda.objects.all()

        ordenacao = request.GET.get('ordenacao', '')
        if ordenacao == 'asc':
            demandas_list = demandas_list.order_by('data')
        elif ordenacao == 'desc':
            demandas_list = demandas_list.order_by('-data')

        user_permissions = {
            'view_cadastrar_demanda': request.user.has_perm('sistema_gerenciamento.view_cadastrar_demanda'),
            'view_editar_demanda': request.user.has_perm('sistema_gerenciamento.view_demanda'),
            'view_deletar_demanda': request.user.has_perm('sistema_gerenciamento.view_deletar_demanda'),
        }

        return render(request, 'Demandas_transporte/demandas.html', {'demandas_list': demandas_list, 'user_permissions': user_permissions})


@login_required(login_url="/auth/user_login/")
@permission_required('sistema_gerenciamento.view_cadastrar_demanda',raise_exception=True)
def cadastrar_demanda(request):
    if request.method == 'GET':
        form = DemandaForm
        return render(request, 'Demandas_transporte/cadastrar_demandas.html', {'form': form})
    else:
        form = DemandaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('demandas')
        else:
            return render(request, 'Demandas_transporte/cadastrar_demandas.html', {'form': form})


@login_required(login_url="/auth/user_login/")
@permission_required('sistema_gerenciamento.view_editar_demanda',raise_exception=True)
def editar_demanda(request, demanda_id):
    demanda = get_object_or_404(Demanda, pk=demanda_id)

    if request.method == 'POST':
        form = DemandaForm(request.POST, instance=demanda)
        if form.is_valid():
            form.save()
            return redirect('demanda')
    else:
        form = DemandaForm(instance=demanda)

    return render(request, 'Demandas_transporte/editar_demanda.html', {'form':form ,'demanda':demanda})


@login_required(login_url="/auth/user_login/")
@permission_required('sistema_gerenciamento.view_deletar_demanda',raise_exception=True)
def deletar_demanda(request, demanda_id):
    demanda = get_object_or_404(Demanda, pk=demanda_id)
    demanda.delete()
    return redirect('demandas')


from datetime import datetime

@login_required(login_url="/auth/user_login/")
def viagens(request):
    if request.method == 'GET':
        viagem_list = Viagem.objects.all()

        # Verifique se há um parâmetro de pesquisa de data de saída
        data_saida_filter = request.GET.get('data_saida', None)
        if data_saida_filter:
            # Converta a data fornecida pelo usuário para um objeto de data
            data_saida_filter = datetime.strptime(data_saida_filter, '%Y-%m-%d').date()
            # Filtrar viagens com a data de saída fornecida
            viagem_list = viagem_list.filter(data_saida=data_saida_filter)

        ordenacao = request.GET.get('ordenacao', '')
        if ordenacao == 'asc':
            viagem_list = viagem_list.order_by('data_saida')
        elif ordenacao == 'desc':
            viagem_list = viagem_list.order_by('-data_saida')

        user_permissions = {
            'view_cadastrar_viagem': request.user.has_perm('sistema_gerenciamento.view_cadastrar_viagem'),
            'view_editar_viagem': request.user.has_perm('sistema_gerenciamento.view_viagem'),
            'view_deletar_viagem': request.user.has_perm('sistema_gerenciamento.view_deletar_viagem'),
        }

        return render(request, 'viagens/viagens.html', {'viagem_list': viagem_list, 'user_permissions': user_permissions})


@login_required(login_url="/auth/user_login/")
@permission_required('sistema_gerenciamento.view_cadastrar_viagem',raise_exception=True)
def cadastrar_viagem(request):
    if request.method == 'GET':
        form = ViagemForm
        return render(request, 'viagens/cadastrar_viagem.html', {'form': form})
    else:
        form = ViagemForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('viagens')
        else:
            return render(request, 'viagens/cadastrar_viagem.html', {'form': form})


@login_required(login_url="/auth/user_login/")
@permission_required('sistema_gerenciamento.view_editar_viagem',raise_exception=True)
def editar_viagem(request, viagem_id):
    viagem = get_object_or_404(Viagem, pk=viagem_id)

    if request.method == 'POST':
        form = ViagemForm(request.POST, instance=viagem)
        if form.is_valid():
            form.save()
            return redirect('viagens')
    else:
        form = ViagemForm(instance=viagem)

    return render(request, 'viagens/editar_viagem.html', {'form': form, 'viagem': viagem})


@login_required(login_url="/auth/user_login/")
@permission_required('sistema_gerenciamento.view_deletar_viagem',raise_exception=True)
def deletar_viagem(request, viagem_id):
    viagem = get_object_or_404(Viagem, pk=viagem_id)
    viagem.delete()
    return redirect('viagens')


#-----------------------------------------------------------------------------------------------------------------------


#Relatórios

def dashborad(request):
    if request.method == "GET":
        return render(request, 'dashboard/dashboard.html')