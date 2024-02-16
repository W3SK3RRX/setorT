from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, \
    PasswordResetCompleteView
from django.urls import path
from . import views
from .views import (editar_veiculo, deletar_veiculo, editar_manutencao, deletar_manutencao, view_comprovante,
                    view_comprovante_checklist, editar_checklist, deletar_checklist, visualizar_documentos, editar_motorista, deletar_motorista,
                    view_comprovante_abastecimento, editar_abastecimento, deletar_abastecimento, editar_rota, deletar_rota,
                    editar_demanda, deletar_demanda, editar_viagem, deletar_viagem)

urlpatterns = [

    path('cadastro/', views.cadastro, name='cadastro'),
    path('', views.user_login, name='user_login'),
    path('logout_user/', views.user_logout, name='logout_user'),
    path('home/', views.home, name='home'),


    #recuperação de senha
    path('auth/password_reset/', PasswordResetView.as_view(), name='password_reset'),
    path('auth/password_reset/done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('auth/reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('auth/reset/done/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),


    #Veículos
    path('home/veiculos/', views.veiculos, name='veiculos'),
    path('home/veiculos/cadastrar_veiculos', views.cadastrar_veiculos, name='cadastrar_veiculos'),
    path('home/veiculos/editar_veiculo/<int:veiculo_id>', editar_veiculo, name='editar_veiculo'),
    path('home/veiculos/deletar_veiculo/<int:veiculo_id>', deletar_veiculo, name='deletar_veiculo'),


    #Veículos/Manutenções
    path('home/veiculos/manutencao', views.manutencao, name='manutencao'),
    path('home/veiculos/<int:veiculo_id>/manutencoes/', views.manutencoes_veiculo, name='manutencoes_veiculo'),
    path('home/veiculos/manutencao/cadastrar_manutencao', views.cadastrar_manutencao, name='cadastrar_manutencao'),
    path('home/view_comprovante/<int:manutencao_id>/', view_comprovante, name='view_comprovante'),
    path('home/veiculos/manutencao/editar_manutencao/<int:manutencao_id>', editar_manutencao, name='editar_manutencao'),
    path('home/veiculos/manutencao/deletar_manutencao/<int:manutencao_id>', deletar_manutencao, name='deletar_manutencao'),


    #Veículos/checklists
    path('home/veiculos/checklists', views.checklists, name='checklists'),
    path('home/veiculos/checklists/cadastrar_checklist', views.cadastrar_checklist, name='cadastrar_checklist'),
    path('home/view_comprovante_checklist/<int:checklist_id>/', view_comprovante_checklist, name='view_comprovante_checklist'),
    path('home/veiculos/checklists/editar_checklist/<int:checklist_id>', editar_checklist, name='editar_checklist'),
    path('home/veiculos/checklist/deletar_checklist/<int:checklist_id>', deletar_checklist, name='deletar_checklist'),


    #Motoristas
    path('home/motoristas', views.motoristas, name='motoristas'),
    path('home/motoristas/cadastrar_motorista', views.cadastrar_motorista, name='cadastrar_motorista'),
    path('home/visualizar_documentos/<int:motorista_id>/', visualizar_documentos, name='visualizar_documentos'),
    path('home/motoristas/editar_motorista/<int:motorista_id>', editar_motorista, name='editar_motorista'),
    path('home/motoristas/deletar_motorista/<int:motorista_id>', deletar_motorista, name='deletar_motorista'),


    #rotas
    path('home/rotas', views.rotas, name="rotas"),
    path('home/rotas/cadastrar_rota', views.cadastrar_rota, name="cadastrar_rota"),
    path('home/rotas/editar_rota/<int:rota_id>', editar_rota, name='editar_rota'),
    path('home/rotas/deletar_rota/<int:rota_id>', deletar_rota, name='deletar_rota'),


    #Combutivel
    path('home/combustivel', views.combustivel, name='combustivel'),
    path('home/combustivel/cadastrar_abastecimento', views.cadastrar_abastecimento, name='cadastrar_abastecimento'),
    path('home/view_comprovante_abastecimento/<int:abastecimento_id>/', view_comprovante_abastecimento, name='view_comprovante_abastecimento'),
    path('home/combustivel/editar_abastecimento/<int:abastecimento_id>', editar_abastecimento, name='editar_abastecimento'),
    path('home/combustivel/deletar_abastecimento/<int:abastecimento_id>', deletar_abastecimento, name='deletar_abastecimento'),


    #Demandas_transporte
    path('home/demandas', views.demandas, name='demandas'),
    path('home/demandas/cadastrar_demanda', views.cadastrar_demanda, name='cadastrar_demanda'),
    path('home/demandas/editar_demanda/<int:demanda_id>', editar_demanda, name="editar_demanda"),
    path('home/demandas/deletar/<int:demanda_id>', deletar_demanda, name="deletar_demanda"),


    #viagens
    path('home/viagens', views.viagens, name='viagens'),
    path('home/viagens/cadastrar_viagem', views.cadastrar_viagem, name='cadastrar_viagem'),
    path('home/viagens/editar_viagem/<int:viagem_id>', editar_viagem, name="editar_viagem"),
    path('home/viagens/deletar_viagem/<int:viagem_id>', deletar_viagem, name="deletar_viagem"),


    #Relatórios
    path('home/dashboard', views.dashborad, name='dashboard')

]
