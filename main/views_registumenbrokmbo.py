# views_registumenbrokmbo.py (atuailza ho chart data)
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q, Count
from .models import RegistuMenbroKmbo, POSTO_CHOICES, SERVISU_CHOICES, GENERU_CHOICES, MUNICIPIOS_TIMOR_LESTE, HABILITASAUN_CHOICES, FATIN_SERVISU_CHOICES, IDADE_CHOICES
from .forms import RegistuMenbroKmboModelForm
from main.utils import decrypt_id
import json
import csv
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from django.http import HttpResponse
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from datetime import datetime
import io

def listaregistumenbrokmbo(request):
    registumenbrokmbo = RegistuMenbroKmbo.objects.all().order_by('-data_rejistu')
    
    # ===== ESTATISTIKA BÁZIKU =====
    total_membro = registumenbrokmbo.count()
    total_feto = registumenbrokmbo.filter(generu='FETO').count()
    total_mane = registumenbrokmbo.filter(generu='MANE').count()
    
    percentual_feto = round((total_feto / total_membro * 100), 1) if total_membro > 0 else 0
    percentual_mane = round((total_mane / total_membro * 100), 1) if total_membro > 0 else 0
    
    total_eleitoral = registumenbrokmbo.filter(tipu_dokumentu='ELEITORAL').count()
    total_bi = registumenbrokmbo.filter(tipu_dokumentu='BI').count()

    color_palette = [
        '#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEEAD',
        '#D4A5A5', '#9B59B6', '#3498DB', '#E67E22', '#2ECC71',
        '#F1C40F', '#E74C3C', '#1ABC9C', '#E67E22', '#95A5A6'
    ]
    
    # ===== GENERU =====
    chart_generu_labels = json.dumps(['Feto', 'Mane'])
    chart_generu_data = json.dumps([total_feto, total_mane])
    chart_generu_colors = json.dumps(['#dc3545', '#007bff'])
    
    # ===== POSTU (ho dadus habilitasaun) =====
    posto_data = []
    posto_labels = []
    posto_stats_full = []
    
    for posto_code, posto_name in POSTO_CHOICES:
        membros_posto = registumenbrokmbo.filter(posto=posto_code)
        total = membros_posto.count()
        if total > 0:
            posto_labels.append(posto_name[:10] + '...' if len(posto_name) > 10 else posto_name)
            posto_data.append(total)
            
            feto = membros_posto.filter(generu='FETO').count()
            mane = membros_posto.filter(generu='MANE').count()
            percentual = round((total / total_membro * 100), 1) if total_membro > 0 else 0
            
            # Habilitasaun
            s1 = membros_posto.filter(habilitasaun_literaria='S1').count()
            s2 = membros_posto.filter(habilitasaun_literaria='S2').count()
            s3 = membros_posto.filter(habilitasaun_literaria='S3').count()
            sma = membros_posto.filter(habilitasaun_literaria='SMA').count()
            sd = membros_posto.filter(habilitasaun_literaria='SD').count()
            total_known = s1 + s2 + s3 + sma + sd
            seluk = total - total_known
            
            posto_stats_full.append({
                'nome': posto_name,
                'total': total,
                'feto': feto,
                'mane': mane,
                'percentual': percentual,
                's1': s1,
                's2': s2,
                's3': s3,
                'sma': sma,
                'sd': sd,
                'seluk': seluk,
            })
    
    chart_postu_labels = json.dumps(posto_labels)
    chart_postu_data = json.dumps(posto_data)
    chart_postu_colors = json.dumps(color_palette[:len(posto_data)])
    
    # Top Postu
    top_posto = max(posto_stats_full, key=lambda x: x['total']) if posto_stats_full else {'nome': 'Laiha', 'total': 0, 'percentual': 0}
    top_postu_list = sorted(posto_stats_full, key=lambda x: x['total'], reverse=True)
    posto_stats_mini = posto_stats_full[:10]   # hatudu top 10 (aumenta)
    
    # ===== TIPU SERVISU =====
    servisu_data = []
    servisu_labels = []
    servisu_stats_full = []
    
    for serv_code, serv_name in SERVISU_CHOICES:
        total = registumenbrokmbo.filter(servisu_hanesan=serv_code).count()
        if total > 0:
            servisu_labels.append(serv_name[:15] + '...' if len(serv_name) > 15 else serv_name)
            servisu_data.append(total)
            
            percentual = round((total / total_membro * 100), 1) if total_membro > 0 else 0
            servisu_stats_full.append({
                'tipo': serv_name,
                'total': total,
                'percentual': percentual
            })
    
    chart_servisu_labels = json.dumps(servisu_labels)
    chart_servisu_data = json.dumps(servisu_data)
    chart_servisu_colors = json.dumps(color_palette[:len(servisu_data)])
    servisu_stats_mini = sorted(servisu_stats_full, key=lambda x: x['total'], reverse=True)[:10]
    
    # ===== FATIN SERVISU =====
    fatin_servisu_data = []
    fatin_servisu_labels = []
    
    for fatin_code, fatin_name in FATIN_SERVISU_CHOICES:
        total = registumenbrokmbo.filter(fatin_servisu=fatin_code).count()
        fatin_servisu_labels.append(fatin_name)
        fatin_servisu_data.append(total)
    
    chart_fatin_servisu_labels = json.dumps(fatin_servisu_labels)
    chart_fatin_servisu_data = json.dumps(fatin_servisu_data)
    chart_fatin_servisu_colors = json.dumps(color_palette[:len(fatin_servisu_data)])
    
    # ===== IDADE =====
    idade_data = []
    idade_labels = []
    
    for idade_code, idade_name in IDADE_CHOICES:
        total = registumenbrokmbo.filter(idade=idade_code).count()
        idade_labels.append(idade_name)
        idade_data.append(total)
    
    chart_idade_labels = json.dumps(idade_labels)
    chart_idade_data = json.dumps(idade_data)
    chart_idade_colors = json.dumps(color_palette[:len(idade_data)])
    
    # ===== HABILITASAUN LITERARIA =====
    habilitasaun_data = []
    habilitasaun_labels = []
    
    for hab_code, hab_name in HABILITASAUN_CHOICES:
        total = registumenbrokmbo.filter(habilitasaun_literaria=hab_code).count()
        hab_name_short = hab_name[:10] + '...' if len(hab_name) > 10 else hab_name
        habilitasaun_labels.append(hab_name_short)
        habilitasaun_data.append(total)
    
    chart_habilitasaun_labels = json.dumps(habilitasaun_labels)
    chart_habilitasaun_data = json.dumps(habilitasaun_data)
    chart_habilitasaun_colors = json.dumps(color_palette[:len(habilitasaun_data)])
    
    # ===== HELA FATIN ATUAL =====
    hela_fatin_data = []
    hela_fatin_labels = []
    
    for mun_code, mun_name in MUNICIPIOS_TIMOR_LESTE:
        total = registumenbrokmbo.filter(hela_fatin_atual=mun_code).count()
        if total > 0:
            hela_fatin_labels.append(mun_name)
            hela_fatin_data.append(total)
    
    chart_hela_fatin_labels = json.dumps(hela_fatin_labels)
    chart_hela_fatin_data = json.dumps(hela_fatin_data)
    chart_hela_fatin_colors = json.dumps(color_palette[:len(hela_fatin_data)])
    
    # ===== PROFISAUN DETALLU =====
    chart_profisaun_detallu_labels = json.dumps(servisu_labels)
    chart_profisaun_detallu_data = json.dumps(servisu_data)
    chart_profisaun_detallu_colors = json.dumps(color_palette[:len(servisu_data)])
    
    # ===== MATRIZ POSTU X SERVISU (ba tabela profisaun) =====
    servico_codes = ['GOVERNU', 'LAOS_GOVERNU', 'POLISIA_FDTL', 'DOUTOR',
                     'DOSENTE', 'PROFESOR', 'GOVERNNANTE', 'SETOR_PRIVADO',
                     'REFORMADO', 'TRABLHADOR']
    posto_servico_matrix = []
    for posto_code, posto_name in POSTO_CHOICES:
        membros_posto = registumenbrokmbo.filter(posto=posto_code)
        total_posto = membros_posto.count()
        if total_posto == 0:
            continue
        row = {
            'posto_nome': posto_name,
            'total': total_posto,
            'percentual': round((total_posto / total_membro * 100), 1) if total_membro > 0 else 0,
        }
        for serv_code in servico_codes:
            row[serv_code] = membros_posto.filter(servisu_hanesan=serv_code).count()
        posto_servico_matrix.append(row)
    posto_servico_matrix = sorted(posto_servico_matrix, key=lambda x: x['total'], reverse=True)
    
    # ===== ESTATISTIKA ADISIONAL =====
    total_superior = registumenbrokmbo.filter(
        Q(habilitasaun_literaria='S1') | 
        Q(habilitasaun_literaria='S2') | 
        Q(habilitasaun_literaria='S3')
    ).count()
    percentual_superior = round((total_superior / total_membro * 100), 1) if total_membro > 0 else 0
    
    total_nasional = registumenbrokmbo.filter(fatin_servisu='NASIONAL').count()
    total_rai_liur = registumenbrokmbo.filter(
        Q(fatin_servisu='EUROPA') |
        Q(fatin_servisu='KOREA') |
        Q(fatin_servisu='AUSTRALIA') |
        Q(fatin_servisu='NEW ZELANDIA') |
        Q(fatin_servisu='SELUK')
    ).count()
    
    # ===== REKOMENDASAUN =====
    rekomendasaun_list = []
    for posto in posto_stats_full:
        if posto['total'] < 5:
            rekomendasaun_list.append(f"Postu <strong>{posto['nome']}</strong> presiza rekruta membru foun (ohin {posto['total']} deit)")
    if total_feto < total_mane * 0.5:
        rekomendasaun_list.append(f"Presiza aumenta partisipasaun <strong>feto</strong> (feto {percentual_feto}%, mane {percentual_mane}%)")
    if total_superior < total_membro * 0.3:
        rekomendasaun_list.append(f"Enkoraja membro atu <strong>kontinua estudu</strong> (ohin {percentual_superior}% deit iha ensinu superior)")
    if total_rai_liur < 5:
        rekomendasaun_list.append(f"Identifika <strong>membro ne'ebé servisu iha rai liur</strong> atu expande network (ohin {total_rai_liur} deit)")
    kontaktu_lack = registumenbrokmbo.filter(Q(telefone__isnull=True) | Q(telefone='')).count()
    if kontaktu_lack > 0:
        rekomendasaun_list.append(f"Atualiza <strong>kontaktu telefone</strong> ba membru {kontaktu_lack} pessoa")
    
    context = {
        "registupartisipante": registumenbrokmbo,
        
        "total_membro": total_membro,
        "total_feto": total_feto,
        "total_mane": total_mane,
        "percentual_feto": percentual_feto,
        "percentual_mane": percentual_mane,
        "total_eleitoral": total_eleitoral,
        "total_bi": total_bi,
        
        # Chart data (ho kór)
        "chart_generu_labels": chart_generu_labels,
        "chart_generu_data": chart_generu_data,
        "chart_generu_colors": chart_generu_colors,
        
        "chart_postu_labels": chart_postu_labels,
        "chart_postu_data": chart_postu_data,
        "chart_postu_colors": chart_postu_colors,
        
        "chart_servisu_labels": chart_servisu_labels,
        "chart_servisu_data": chart_servisu_data,
        "chart_servisu_colors": chart_servisu_colors,
        
        "chart_fatin_servisu_labels": chart_fatin_servisu_labels,
        "chart_fatin_servisu_data": chart_fatin_servisu_data,
        "chart_fatin_servisu_colors": chart_fatin_servisu_colors,
        
        "chart_idade_labels": chart_idade_labels,
        "chart_idade_data": chart_idade_data,
        "chart_idade_colors": chart_idade_colors,
        
        "chart_habilitasaun_labels": chart_habilitasaun_labels,
        "chart_habilitasaun_data": chart_habilitasaun_data,
        "chart_habilitasaun_colors": chart_habilitasaun_colors,
        
        "chart_hela_fatin_labels": chart_hela_fatin_labels,
        "chart_hela_fatin_data": chart_hela_fatin_data,
        "chart_hela_fatin_colors": chart_hela_fatin_colors,
        
        "chart_profisaun_detallu_labels": chart_profisaun_detallu_labels,
        "chart_profisaun_detallu_data": chart_profisaun_detallu_data,
        "chart_profisaun_detallu_colors": chart_profisaun_detallu_colors,
        
        # Estatistika tabela
        "posto_stats_mini": posto_stats_mini,
        "top_posto": top_posto,
        "top_postu_list": top_postu_list,
        "servisu_stats_mini": servisu_stats_mini,
        "posto_servico_matrix": posto_servico_matrix,   # <-- importante ba tabela rua
        
        # Estatistika adisional
        "total_superior": total_superior,
        "percentual_superior": percentual_superior,
        "total_nasional": total_nasional,
        "total_rai_liur": total_rai_liur,
        
        "rekomendasaun_list": rekomendasaun_list[:5],
    }
    return render(request, "registumenbrokmbo/lista.html", context)

def inputregistumenbrokmbo(request):
    if request.method == "POST":
        form = RegistuMenbroKmboModelForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                # Salva form, husi save() sei retorna objetu ne'ebe salva
                partisipante = form.save()
                
                # Fo mensagem detalhada wainhira susesu
                messages.success(
                    request, 
                    f"✅ Obrigado, Ita Rejistu ho Susessu!\nNaran Kompletu: {partisipante.naran_kompletu}, Posto: {partisipante.get_posto_display()}"
                )
                return redirect('menbrokmbo')
            except Exception as e:
                messages.error(request, f"❌ Error atu rai dadus: {str(e)}")
        else:
            # Hatudu error sira ho klaru
            error_messages = []
            for field, errors in form.errors.items():
                for error in errors:
                    field_label = form.fields[field].label if field in form.fields else field
                    error_messages.append(f"⚠️ {field_label}: {error}")
            
            if error_messages:
                full_message = "\n\n".join(error_messages)
                messages.error(request, f"❌ Validasaun Falha:\n{full_message}")
    else:
        form = RegistuMenbroKmboModelForm()
    
    context = {
        'form': form
    }
    return render(request, "registumenbrokmbo/input.html", context)

def updateregistumenbrokmbo(request, id):
    try:
        ide = decrypt_id(id)
        registumenbrokmbo = get_object_or_404(RegistuMenbroKmbo, id=ide)
    except:
        messages.error(request, "❌ ID invalidu!")
        return redirect('listaregistumenbrokmbo')
    
    if request.method == "POST":
        form = RegistuMenbroKmboModelForm(request.POST, request.FILES, instance=registumenbrokmbo)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, "✅ Dadus Atualiza ho Susessu!")
                return redirect('listaregistumenbrokmbo')
            except Exception as e:
                messages.error(request, f"❌ Error atu atualiza: {str(e)}")
        else:
            error_messages = []
            for field, errors in form.errors.items():
                for error in errors:
                    if len(error) > 100:
                        error_messages.append(f"\n{error}")
                    else:
                        field_label = form.fields[field].label if field in form.fields else field
                        error_messages.append(f"⚠️ {field_label}: {error}")
            
            if error_messages:
                full_message = "\n\n".join(error_messages)
                messages.error(request, f"❌ Atualizasaun Falha:\n{full_message}")
    else:
        form = RegistuMenbroKmboModelForm(instance=registumenbrokmbo)
    
    context = {
        'form': form
    }
    return render(request, "registumenbrokmbo/update.html", context)

def hamosregistumenbrokmbo(request, id):
    try:
        ide = decrypt_id(id)
        registumenbrokmbo = get_object_or_404(RegistuMenbroKmbo, id=ide)
        naran = registumenbrokmbo.naran_kompletu
        registumenbrokmbo.delete()
        messages.success(request, f"✅ Dadus '{naran}' Apaga ho Susessu!")
    except:
        messages.error(request, "❌ Error atu apaga dadus!")
    return redirect('listaregistumenbrokmbo')


def show(request):
    registumenbrokmbo = RegistuMenbroKmbo.objects.all().order_by('-data_rejistu')
    total = registumenbrokmbo.count()

    # Função atu prepara dadus ba chart (mantén hanesan)
    def prepare_chart_data(queryset, field, choices_dict):
        stats = queryset.values(field).annotate(count=Count(field)).order_by('-count')
        labels = []
        data = []
        colors = []
        
        color_palette = [
            '#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEEAD',
            '#D4A5A5', '#9B59B6', '#3498DB', '#E67E22', '#2ECC71',
            '#F1C40F', '#E74C3C', '#1ABC9C', '#E67E22', '#95A5A6'
        ]
        
        for i, item in enumerate(stats):
            if item[field]:
                label = choices_dict.get(item[field], item[field])
                labels.append(label)
                data.append(item['count'])
                colors.append(color_palette[i % len(color_palette)])
        
        return labels, data, colors

    # Dictionary ba choices
    generu_dict = dict(GENERU_CHOICES)
    postu_dict = dict(POSTO_CHOICES)
    servisu_dict = dict(SERVISU_CHOICES)
    hela_fatin_dict = dict(MUNICIPIOS_TIMOR_LESTE)
    habilitasaun_dict = dict(HABILITASAUN_CHOICES)
    fatin_servisu_dict = dict(FATIN_SERVISU_CHOICES)
    idade_dict = dict(IDADE_CHOICES)

    # Prepara dadus ho kores (ba pie charts)
    generu_labels, generu_data, generu_colors = prepare_chart_data(registumenbrokmbo, 'generu', generu_dict)
    postu_labels, postu_data, postu_colors = prepare_chart_data(registumenbrokmbo, 'posto', postu_dict)
    servisu_labels, servisu_data, servisu_colors = prepare_chart_data(registumenbrokmbo, 'servisu_hanesan', servisu_dict)
    hela_fatin_labels, hela_fatin_data, hela_fatin_colors = prepare_chart_data(registumenbrokmbo, 'hela_fatin_atual', hela_fatin_dict)
    habilitasaun_labels, habilitasaun_data, habilitasaun_colors = prepare_chart_data(registumenbrokmbo, 'habilitasaun_literaria', habilitasaun_dict)
    fatin_servisu_labels, fatin_servisu_data, fatin_servisu_colors = prepare_chart_data(registumenbrokmbo, 'fatin_servisu', fatin_servisu_dict)
    idade_labels, idade_data, idade_colors = prepare_chart_data(registumenbrokmbo, 'idade', idade_dict)

    # ===== ESTATISTIKA BA TABELA POSTU (ho edukasaun) =====
    posto_stats_full = []
    for posto_code, posto_name in POSTO_CHOICES:
        membros_posto = registumenbrokmbo.filter(posto=posto_code)
        total_posto = membros_posto.count()
        if total_posto > 0:
            feto = membros_posto.filter(generu='FETO').count()
            mane = membros_posto.filter(generu='MANE').count()
            percentual = round((total_posto / total * 100), 1) if total > 0 else 0
            
            # Konta edukasaun
            s1 = membros_posto.filter(habilitasaun_literaria='S1').count()
            s2 = membros_posto.filter(habilitasaun_literaria='S2').count()
            s3 = membros_posto.filter(habilitasaun_literaria='S3').count()
            sma = membros_posto.filter(habilitasaun_literaria='SMA').count()
            sd = membros_posto.filter(habilitasaun_literaria='SD').count()
            seluk = membros_posto.exclude(habilitasaun_literaria__in=['S1','S2','S3','SMA','SD']).count()
            
            posto_stats_full.append({
                'nome': posto_name,
                'total': total_posto,
                'feto': feto,
                'mane': mane,
                'percentual': percentual,
                's1': s1,
                's2': s2,
                's3': s3,
                'sma': sma,
                'sd': sd,
                'seluk': seluk,
            })
    # Ordena husi ne'ebé boot ba ki'ik no foti top 5
    posto_stats_mini = sorted(posto_stats_full, key=lambda x: x['total'], reverse=True)

    # ===== MATRIZ POSTU X SERVISU (ba tabela profisaun) =====
    posto_servico_matrix = []
    # Lista kódigu servisu tuir koluna ne'ebé ita hakarak
    servico_codes = ['GOVERNU', 'LAOS_GOVERNU', 'POLISIA_FDTL', 'DOUTOR', 
                     'DOSENTE', 'PROFESOR', 'GOVERNNANTE', 'SETOR_PRIVADO', 
                     'REFORMADO', 'TRABLHADOR']
    
    for posto_code, posto_name in POSTO_CHOICES:
        membros_posto = registumenbrokmbo.filter(posto=posto_code)
        total_posto = membros_posto.count()
        if total_posto == 0:
            continue  # Labele hatudu postu ne'ebé la iha membru
        
        row = {
            'posto_nome': posto_name,
            'total': total_posto,
            'percentual': round((total_posto / total * 100), 1) if total > 0 else 0,
        }
        # Preenche kontajen ba kada tipu servisu
        for serv_code in servico_codes:
            count = membros_posto.filter(servisu_hanesan=serv_code).count()
            row[serv_code] = count
        
        posto_servico_matrix.append(row)
    
    # Ordena husi total boot ba ki'ik
    posto_servico_matrix = sorted(posto_servico_matrix, key=lambda x: x['total'], reverse=True)

    # Servisu stats full (ba fallback)
    servisu_stats_full = []
    for serv_code, serv_name in SERVISU_CHOICES:
        total_serv = registumenbrokmbo.filter(servisu_hanesan=serv_code).count()
        if total_serv > 0:
            percentual = round((total_serv / total * 100), 1) if total > 0 else 0
            servisu_stats_full.append({
                'tipo': serv_name,
                'total': total_serv,
                'percentual': percentual
            })
    servisu_stats_mini = sorted(servisu_stats_full, key=lambda x: x['total'], reverse=True)[:5]

    # Top Postu (ba card)
    top_posto = max(posto_stats_full, key=lambda x: x['total']) if posto_stats_full else {'nome': 'Laiha', 'total': 0, 'percentual': 0}

    # Total Feto no Mane
    total_feto = registumenbrokmbo.filter(generu='FETO').count()
    total_mane = registumenbrokmbo.filter(generu='MANE').count()
    
    # Estatistika dokumentu
    total_eleitoral = registumenbrokmbo.filter(tipu_dokumentu='ELEITORAL').count()
    total_bi = registumenbrokmbo.filter(tipu_dokumentu='BI').count()

    context = {
        "registupartisipante": registumenbrokmbo,
        "total_membro": total,
        "total_feto": total_feto,
        "total_mane": total_mane,
        "total_eleitoral": total_eleitoral,
        "total_bi": total_bi,
        
        # Dadus ba chart ho kores
        "generu_labels": json.dumps(generu_labels),
        "generu_data": json.dumps(generu_data),
        "generu_colors": json.dumps(generu_colors),
        
        "idade_labels": json.dumps(idade_labels),
        "idade_data": json.dumps(idade_data),
        "idade_colors": json.dumps(idade_colors),
        
        "hela_fatin_labels": json.dumps(hela_fatin_labels),
        "hela_fatin_data": json.dumps(hela_fatin_data),
        "hela_fatin_colors": json.dumps(hela_fatin_colors),
        
        "postu_labels": json.dumps(postu_labels),
        "postu_data": json.dumps(postu_data),
        "postu_colors": json.dumps(postu_colors),
        
        "habilitasaun_labels": json.dumps(habilitasaun_labels),
        "habilitasaun_data": json.dumps(habilitasaun_data),
        "habilitasaun_colors": json.dumps(habilitasaun_colors),
        
        "servisu_labels": json.dumps(servisu_labels),
        "servisu_data": json.dumps(servisu_data),
        "servisu_colors": json.dumps(servisu_colors),
        
        "fatin_servisu_labels": json.dumps(fatin_servisu_labels),
        "fatin_servisu_data": json.dumps(fatin_servisu_data),
        "fatin_servisu_colors": json.dumps(fatin_servisu_colors),
        
        # TOP 3 (ba card)
        "top_postu": json.dumps(postu_labels[:3] if len(postu_labels) >= 3 else postu_labels),
        "top_postu_data": json.dumps(postu_data[:3] if len(postu_data) >= 3 else postu_data),
        "top_servisu": json.dumps(servisu_labels[:3] if len(servisu_labels) >= 3 else servisu_labels),
        "top_servisu_data": json.dumps(servisu_data[:3] if len(servisu_data) >= 3 else servisu_data),
        
        # Dadus ba tabela mini (Postu no Profisaun)
        "posto_stats_mini": posto_stats_mini,
        "servisu_stats_mini": servisu_stats_mini,
        "posto_servico_matrix": posto_servico_matrix,
        "servico_codes": servico_codes,
        "top_posto": top_posto,
    }

    return render(request, "registumenbrokmbo/show.html", context)




# ===== DOWNLOAD EXCEL =====
def download_registumenbrokmbo_excel(request):
    # Kria workbook
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Membro KMBO"
    
    # Header style
    header_font = Font(bold=True, color="FFFFFF")
    header_fill = PatternFill(start_color="1E3C72", end_color="2A5298", fill_type="solid")
    header_alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
    border = Border(
        left=Side(style='thin'), right=Side(style='thin'),
        top=Side(style='thin'), bottom=Side(style='thin')
    )
    
    # Headers
    headers = [
        'Nu', 'Naran Kompletu', 'No. Eleitoral/BI', 'Generu', 'Idade',
        'Postu', 'Hela Fatin Atual', 'Servisu Hanesan', 'Fatin Servisu',
        'Habilitasaun Literaria', 'Telefone', 'Email', 'Data Rejistu'
    ]
    
    for col_num, header in enumerate(headers, 1):
        cell = ws.cell(row=1, column=col_num)
        cell.value = header
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = header_alignment
        cell.border = border
    
    # Data
    registu = RegistuMenbroKmbo.objects.all().order_by('-data_rejistu')
    
    for row_num, partisipante in enumerate(registu, 2):
        ws.cell(row=row_num, column=1).value = row_num - 1
        ws.cell(row=row_num, column=2).value = partisipante.naran_kompletu
        ws.cell(row=row_num, column=3).value = partisipante.nomor_eleitoral_bi
        ws.cell(row=row_num, column=4).value = partisipante.get_generu_display()
        ws.cell(row=row_num, column=5).value = partisipante.idade
        ws.cell(row=row_num, column=6).value = partisipante.get_posto_display()
        ws.cell(row=row_num, column=7).value = partisipante.get_hela_fatin_atual_display()
        ws.cell(row=row_num, column=8).value = partisipante.get_servisu_hanesan_display()
        ws.cell(row=row_num, column=9).value = partisipante.get_fatin_servisu_display()
        ws.cell(row=row_num, column=10).value = partisipante.get_habilitasaun_literaria_display()
        ws.cell(row=row_num, column=11).value = partisipante.telefone or '-'
        ws.cell(row=row_num, column=12).value = partisipante.email or '-'
        ws.cell(row=row_num, column=13).value = partisipante.data_rejistu.strftime('%d/%m/%Y %H:%M')
    
    # Ajusta koluna width
    for col in ws.columns:
        max_length = 0
        column = col[0].column_letter
        for cell in col:
            try:
                if len(str(cell.value)) > max_length:
                    max_length = len(str(cell.value))
            except:
                pass
        adjusted_width = min(max_length + 2, 50)
        ws.column_dimensions[column].width = adjusted_width
    
    # Response
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename=membro_kmbo_{}.xlsx'.format(
        datetime.now().strftime('%Y%m%d_%H%M%S')
    )
    
    wb.save(response)
    return response


# ===== DOWNLOAD CSV =====
def download_registumenbrokmbo_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=membro_kmbo_{}.csv'.format(
        datetime.now().strftime('%Y%m%d_%H%M%S')
    )
    
    writer = csv.writer(response)
    writer.writerow([
        'Nu', 'Naran Kompletu', 'No. Eleitoral/BI', 'Generu', 'Idade',
        'Postu', 'Hela Fatin Atual', 'Servisu Hanesan', 'Fatin Servisu',
        'Habilitasaun Literaria', 'Telefone', 'Email', 'Data Rejistu'
    ])
    
    registu = RegistuMenbroKmbo.objects.all().order_by('-data_rejistu')
    
    for idx, partisipante in enumerate(registu, 1):
        writer.writerow([
            idx,
            partisipante.naran_kompletu,
            partisipante.nomor_eleitoral_bi,
            partisipante.get_generu_display(),
            partisipante.idade,
            partisipante.get_posto_display(),
            partisipante.get_hela_fatin_atual_display(),
            partisipante.get_servisu_hanesan_display(),
            partisipante.get_fatin_servisu_display(),
            partisipante.get_habilitasaun_literaria_display(),
            partisipante.telefone or '-',
            partisipante.email or '-',
            partisipante.data_rejistu.strftime('%d/%m/%Y %H:%M')
        ])
    
    return response


# ===== DOWNLOAD PDF =====
def download_registumenbrokmbo_pdf(request):
    # Registra fontes (se iha font Timor)
    try:
        pdfmetrics.registerFont(TTFont('Arial', 'arial.ttf'))
    except:
        pass
    
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer, 
        pagesize=landscape(A4),
        rightMargin=20,
        leftMargin=20,
        topMargin=30,
        bottomMargin=20
    )
    
    elements = []
    styles = getSampleStyleSheet()
    
    # Title
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=16,
        alignment=1,  # Center
        spaceAfter=20,
        textColor=colors.HexColor('#1E3C72')
    )
    title = Paragraph("Lista Membro KMBO (Bobonaro Oan)", title_style)
    elements.append(title)
    
    # Subtitle (date)
    date_style = ParagraphStyle(
        'DateStyle',
        parent=styles['Normal'],
        fontSize=10,
        alignment=1,
        spaceAfter=20
    )
    from datetime import datetime
    date_text = "Data: {}".format(datetime.now().strftime('%d/%m/%Y %H:%M'))
    elements.append(Paragraph(date_text, date_style))
    
    # Get data
    registu = RegistuMenbroKmbo.objects.all().order_by('-data_rejistu')
    
    # Table data
    data = []
    # Headers
    headers = [
        'Nu', 'Naran', 'No. Eleitoral', 'Generu', 'Idade', 
        'Postu', 'Hela Fatin', 'Servisu', 'Fatin Servisu', 'Habilitasaun'
    ]
    data.append(headers)
    
    # Body
    for idx, p in enumerate(registu, 1):
        row = [
            str(idx),
            p.naran_kompletu[:20] + '...' if len(p.naran_kompletu) > 20 else p.naran_kompletu,
            p.nomor_eleitoral_bi,
            p.get_generu_display(),
            p.idade,
            p.get_posto_display()[:15] + '...' if len(p.get_posto_display()) > 15 else p.get_posto_display(),
            p.get_hela_fatin_atual_display()[:10],
            p.get_servisu_hanesan_display()[:15] + '...' if len(p.get_servisu_hanesan_display()) > 15 else p.get_servisu_hanesan_display(),
            p.get_fatin_servisu_display(),
            p.get_habilitasaun_literaria_display()
        ]
        data.append(row)
    
    # Create table
    table = Table(data, repeatRows=1)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1E3C72')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 8),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTSIZE', (0, 1), (-1, -1), 7),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    
    # Alternating row colors
    for i in range(1, len(data)):
        if i % 2 == 0:
            bg_color = colors.HexColor('#f2f2f2')
        else:
            bg_color = colors.white
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, i), (-1, i), bg_color),
        ]))
    
    elements.append(table)
    
    # Footer with statistics
    elements.append(Spacer(1, 20))
    stats_style = ParagraphStyle(
        'StatsStyle',
        parent=styles['Normal'],
        fontSize=9,
        alignment=0,
        textColor=colors.HexColor('#2A5298')
    )
    
    total = len(registu)
    total_feto = registu.filter(generu='FETO').count()
    total_mane = registu.filter(generu='MANE').count()
    
    stats_text = "Total Membro: {} | Feto: {} | Mane: {}".format(total, total_feto, total_mane)
    elements.append(Paragraph(stats_text, stats_style))
    
    # Build PDF
    doc.build(elements)
    buffer.seek(0)
    
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=membro_kmbo_{}.pdf'.format(
        datetime.now().strftime('%Y%m%d_%H%M%S')
    )
    
    return response


# ===== DOWNLOAD ESTATISTIKA EXCEL =====
def download_registumenbrokmbo_estatistika_excel(request):
    from django.db.models import Count, Q
    
    wb = openpyxl.Workbook()
    
    # Sheet 1: Overview
    ws1 = wb.active
    ws1.title = "Overview"
    
    # Header
    header_font = Font(bold=True, color="FFFFFF")
    header_fill = PatternFill(start_color="1E3C72", end_color="2A5298", fill_type="solid")
    
    # Total Membro
    total = RegistuMenbroKmbo.objects.count()
    ws1['A1'] = "ESTATISTIKA MEMBRO KMBO"
    ws1['A1'].font = Font(bold=True, size=14)
    ws1.merge_cells('A1:C1')
    
    ws1['A3'] = "Total Membro"
    ws1['B3'] = total
    ws1['A3'].font = Font(bold=True)
    
    # Sheet 2: Distribuisaun Generu
    ws2 = wb.create_sheet("Generu")
    ws2.append(['Generu', 'Total'])
    feto = RegistuMenbroKmbo.objects.filter(generu='FETO').count()
    mane = RegistuMenbroKmbo.objects.filter(generu='MANE').count()
    ws2.append(['Feto', feto])
    ws2.append(['Mane', mane])
    
    # Sheet 3: Distribuisaun Postu
    ws3 = wb.create_sheet("Postu")
    ws3.append(['Postu', 'Total', 'Feto', 'Mane'])
    from .models import POSTO_CHOICES
    for posto_code, posto_name in POSTO_CHOICES:
        total = RegistuMenbroKmbo.objects.filter(posto=posto_code).count()
        feto = RegistuMenbroKmbo.objects.filter(posto=posto_code, generu='FETO').count()
        mane = RegistuMenbroKmbo.objects.filter(posto=posto_code, generu='MANE').count()
        if total > 0:
            ws3.append([posto_name, total, feto, mane])
    
    # Sheet 4: Servisu
    ws4 = wb.create_sheet("Servisu")
    ws4.append(['Tipu Servisu', 'Total'])
    from .models import SERVISU_CHOICES
    for serv_code, serv_name in SERVISU_CHOICES:
        total = RegistuMenbroKmbo.objects.filter(servisu_hanesan=serv_code).count()
        if total > 0:
            ws4.append([serv_name, total])
    
    # Sheet 5: Hela Fatin
    ws5 = wb.create_sheet("Hela Fatin")
    ws5.append(['Munisipiu', 'Total'])
    from .models import MUNICIPIOS_TIMOR_LESTE
    for mun_code, mun_name in MUNICIPIOS_TIMOR_LESTE:
        total = RegistuMenbroKmbo.objects.filter(hela_fatin_atual=mun_code).count()
        if total > 0:
            ws5.append([mun_name, total])
    
    # Format all sheets
    for ws in [ws1, ws2, ws3, ws4, ws5]:
        for col in ws.columns:
            max_length = 0
            column = col[0].column_letter
            for cell in col:
                try:
                    if len(str(cell.value)) > max_length:
                        max_length = len(str(cell.value))
                except:
                    pass
            adjusted_width = min(max_length + 2, 50)
            ws.column_dimensions[column].width = adjusted_width
    
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename=estatistika_kmbo_{}.xlsx'.format(
        datetime.now().strftime('%Y%m%d_%H%M%S')
    )
    
    wb.save(response)
    return response