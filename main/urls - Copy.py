from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

# Remove the grouped imports and import each view file separately
from ...main import views_lingua
from ...main import views_parseirusira
from ...main import views_organograma
from ...main import views_mensajenhusikordenador
from ...main import views_infojeralkmbo
from ...main import views_ekipakmbo
from ...main import views_atividade
from ...main import views_registuvoluntariu
from ...main import views_anunsiu
from ...main import views_noti
from ...main import views_vizaunmisaun
from ...main import views_galeria
from ...main import views_foto
from ...main import views_video
from ...main import views_dokumentusimportantes
from ...main import views_kategoria
from ...main import views_image
from ...main import views_finansiamentunoapoiu
from ...main import views_publikasaunkmbo
from ...main import views_registupartisipante
from ...main import views_kontaktuami 
from ...main import views_artigu
from ...main import views_projetu
from ...main import views_kontaktu
from ...main import views_registumenbrokmbo

urlpatterns = [
    # Organizational Structure vizaun  
    path('lista/organograma/', views_organograma.listaorganograma, name="listaorganograma"),
    path('atualiza/organograma/<str:id>/', views_organograma.updateorganograma, name="updateorganograma"),
    path('organograma/', views_organograma.show, name="showorg"),

    # Anunsiu
    path('input/anunsiu/',views_anunsiu.inputanunsiu, name="inputanunsiu"),
    path('lista/anunsiu/',views_anunsiu.listaanunsiu, name="listaanunsiu"),
    path('atualiza/anunsiu/<str:id>/',views_anunsiu.updateanunsiu, name="updateanunsiu"),
    path('hamos/anunsiu/<str:id>/',views_anunsiu.hamosanunsiu, name="hamosanunsiu"),
    path('anunsiu/', views_anunsiu.showanunsiu, name="showanunsiu"),
   
    path('vizaun_misaun/', views_vizaunmisaun.vizaunmisaun, name="listavm"),
    path('vizaun_misaun/update/<str:id>/', views_vizaunmisaun.updatevm, name="updatevm"),
    path('vizaun/misaun/', views_vizaunmisaun.show, name="showvm"),

    # System Management ekipa
    path('lista/kategoria/', views_kategoria.listakategoria, name="listakategoria"),
    path('input/kategoria/', views_kategoria.inputkategoria, name="inputkategoria"),
    path('atualiza/kategoria/<int:id>/', views_kategoria.updatekategoria, name="updatekategoria"),
    path('hamos/kategoria/<int:id>/', views_kategoria.hamoskategoria, name="hamoskategoria"),

    path('lingua/', views_lingua.lingua, name="lingua"),
    path('lingua/input/', views_lingua.inputlingua, name="inputlingua"),
    path('lingua/update/<int:id>', views_lingua.update, name="update"),
    path('lingua/hamos/<int:id>', views_lingua.hamos, name="hamos"),

    path('imajen/', views_image.imajen, name="imajen"),
    path('imajen/input/', views_image.inputimajen, name="inputimajen"),
    path('imajen/update/<int:id>', views_image.update, name="updateimajen"),
    path('imajen/hamos/<int:id>', views_image.hamos, name="hamosimajen"),

    path('input/mensajenhusikordenador/', views_mensajenhusikordenador.inputmensajenhusikordenador, name="inputmensajenhusikordenador"),
    path('lista/mensajenhusikordenador/', views_mensajenhusikordenador.listamensajenhusikordenador, name="listamensajenhusikordenador"),
    path('atualiza/mensajenhusikordenador/<str:id>/', views_mensajenhusikordenador.updatemensajenhusikordenador, name="updatemensajenhusikordenador"),
    path('hamos/mensajenhusikordenador/<str:id>/', views_mensajenhusikordenador.hamosmensajenhusikordenador, name="hamosmensajenhusikordenador"),

    path('input/infojeralkmbo/', views_infojeralkmbo.inputinfojeralkmbo, name="inputinfojeralkmbo"),
    path('lista/infojeralkmbo/', views_infojeralkmbo.listainfojeralkmbo, name="listainfojeralkmbo"),
    path('atualiza/infojeralkmbo/<str:id>/', views_infojeralkmbo.updateinfojeralkmbo, name="updateinfojeralkmbo"),
    path('hamos/infojeralkmbo/<str:id>/', views_infojeralkmbo.hamosinfojeralkmbo, name="hamosinfojeralkmbo"),

    path('input/ekipakmbo/', views_ekipakmbo.inputekipakmbo, name="inputekipakmbo"),
    path('lista/ekipakmbo/', views_ekipakmbo.listaekipakmbo, name="listaekipakmbo"),
    path('atualiza/ekipakmbo/<str:id>/', views_ekipakmbo.updateekipakmbo, name="updateekipakmbo"),
    path('hamos/ekipakmbo/<str:id>/', views_ekipakmbo.hamosekipakmbo, name="hamosekipakmbo"),
    path('ekipakmbo/', views_ekipakmbo.show, name="showekipakmbo"),
    # Programs and atividade programa
    
    path('input/finansiamentunoapoiu/', views_finansiamentunoapoiu.inputfinansiamentunoapoiu, name="inputfinansiamentunoapoiu"),
    path('lista/finansiamentunoapoiu/', views_finansiamentunoapoiu.listafinansiamentunoapoiu, name="listafinansiamentunoapoiu"),
    path('atualiza/finansiamentunoapoiu/<str:id>/', views_finansiamentunoapoiu.updatefinansiamentunoapoiu, name="updatefinansiamentunoapoiu"),
    path('hamos/finansiamentunoapoiu/<str:id>/', views_finansiamentunoapoiu.hamosfinansiamentunoapoiu, name="hamosfinansiamentunoapoiu"),

    path('input/publikasaunkmbo/', views_publikasaunkmbo.inputpublikasaunkmbo, name="inputpublikasaunkmbo"),
    path('lista/publikasaunkmbo/', views_publikasaunkmbo.listapublikasaunkmbo, name="listapublikasaunkmbo"),
    path('atualiza/publikasaunkmbo/<str:id>/', views_publikasaunkmbo.updatepublikasaunkmbo, name="updatepublikasaunkmbo"),
    path('hamos/publikasaunkmbo/<str:id>/', views_publikasaunkmbo.hamospublikasaunkmbo, name="hamospublikasaunkmbo"),

    path('input/dokumentusimportantes/', views_dokumentusimportantes.inputdokumentusimportantes, name="inputdokumentusimportantes"),
    path('lista/dokumentusimportantes/', views_dokumentusimportantes.listadokumentusimportantes, name="listadokumentusimportantes"),
    path('atualiza/dokumentusimportantes/<str:id>/', views_dokumentusimportantes.updatedokumentusimportantes, name="updatedokumentusimportantes"),
    path('hamos/dokumentusimportantes/<str:id>/', views_dokumentusimportantes.hamosdokumentusimportantes, name="hamosdokumentusimportantes"),

    # Partners atividade artigu showatividade
    path('inputparseirusira/', views_parseirusira.inputparseirusira, name="inputparseirusira"),
    path('lista/parseirusira/', views_parseirusira.listaparseirusira, name="listaparseirusira"),
    path('atualiza/parseirusira/<str:id>/', views_parseirusira.updateparseirusira, name="updateparseirusira"),
    path('hamos/parseirusira/<str:id>/', views_parseirusira.hamosparseirusira, name="hamosparseirusira"),

   path('input/projetu/', views_projetu.inputprojetu, name="inputprojetu"),
    path('lista/projetu/', views_projetu.listaprojetu, name="listaprojetu"),
    path('atualiza/projetu/<str:id>/', views_projetu.updateprojetu, name="updateprojetu"),
    path('hamos/projetu/<str:id>/', views_projetu.hamosprojetu, name="hamosprojetu"),
    path('projetu/', views_projetu.show, name="showprojetu"),

    
    path('inputatividade/', views_atividade.inputatividade, name="inputatividade"),
    path('lista/atividade/', views_atividade.listaatividade, name="listaatividade"),
    path('atualiza/atividade/<str:id>/', views_atividade.updateatividade, name="updateatividade"),
    path('hamos/atividade/<str:id>/', views_atividade.hamosatividade, name="hamosatividade"),
    path('atividade/', views_atividade.showatividade, name="showatividade"),

    
    # Registration listaatividade
    path('input/registupartisipante/', views_registupartisipante.inputregistupartisipante, name="inputregistupartisipante"),
    path('lista/registupartisipante/', views_registupartisipante.listaregistupartisipante, name="listaregistupartisipante"),
    path('atualiza/registupartisipante/<str:id>/', views_registupartisipante.updateregistupartisipante, name="updateregistupartisipante"),
    path('hamos/registupartisipante/<str:id>/', views_registupartisipante.hamosregistupartisipante, name="hamosregistupartisipante"),
    path('delgadu/', views_registupartisipante.show, name="listadelgadu"),


    path('input/registumenbrokmbo/', views_registumenbrokmbo.inputregistumenbrokmbo, name="inputregistumenbrokmbo"),
    path('lista/registumenbrokmbo/', views_registumenbrokmbo.listaregistumenbrokmbo, name="listaregistumenbrokmbo"),
    path('atualiza/registumenbrokmbo/<str:id>/', views_registumenbrokmbo.updateregistumenbrokmbo, name="updateregistumenbrokmbo"),
    path('hamos/registumenbrokmbo/<str:id>/', views_registumenbrokmbo.hamosregistumenbrokmbo, name="hamosregistumenbrokmbo"),
    path('menbrokmbo/', views_registumenbrokmbo.show, name="menbrokmbo"),

    # path('download-registumenbrokmbo-excel/', views_registumenbrokmbo.download_registumenbrokmbo_excel, name='download_registumenbrokmbo_excel'),
    # path('download-registumenbrokmbo-csv/', views_registumenbrokmbo.download_registumenbrokmbo_csv, name='download_registumenbrokmbo_csv'),
    # path('download-registumenbrokmbo-pdf/', views_registumenbrokmbo.download_registumenbrokmbo_pdf, name='download_registumenbrokmbo_pdf'),
    # path('download-registumenbrokmbo-estatistika-excel/', views_registumenbrokmbo.download_registumenbrokmbo_estatistika_excel, name='download_registumenbrokmbo_estatistika_excel'),




    path('input/registuvoluntariu/', views_registuvoluntariu.inputregistuvoluntariu, name="inputregistuvoluntariu"),
    path('lista/registuvoluntariu/', views_registuvoluntariu.listaregistuvoluntariu, name="listaregistuvoluntariu"),
    path('atualiza/registuvoluntariu/<str:id>/', views_registuvoluntariu.updateregistuvoluntariu, name="updateregistuvoluntariu"),
    path('hamos/registuvoluntariu/<str:id>/', views_registuvoluntariu.hamosregistuvoluntariu, name="hamosregistuvoluntariu"),

    path('lista/kontaktuami/', views_kontaktuami.listakontaktuami, name="listakontaktuami"),
    path('atualiza/kontaktuami/<str:id>/', views_kontaktuami.updatekontaktuami, name="updatekontaktuami"),

     #Kategoria projetu
    path('lista/kategoria/', views_kategoria.listakategoria, name="listakategoria"),
    path('input/kategoria/', views_kategoria.inputkategoria, name="inputkategoria"),
    path('atualiza/kategoria/<str:id>/', views_kategoria.updatekategoria, name="updatekategoria"),
    path('hamos/kategoria/<int:id>/',views_kategoria.hamoskategoria, name="hamoskategoria"),

 #imajen video
    path('imajen/', views_image.imajen, name="imajen"),
    path('imajen/input/', views_image.inputimajen, name="inputimajen"),
    path('imajen/update/<str:id>', views_image.update, name="updateimajen"),
    path('imajen/hamos/<int:id>', views_image.hamos, name="hamosimajen"),
    #notisia
    path('notisia/',views_noti.listanoti, name="listanoti"),
    path('input/notisia/',views_noti.inputnoti, name="inputnoti"),
    path('shownotisia/<slug:slug>/',views_noti.shownotisia, name="shownotisia"),
    path('notisia/detallu/<str:id>/',views_noti.detailnotisia, name="detallu"),
    path('editor/<str:id>',views_noti.editor, name="editor"),
    path('show1/',views_noti.shownotisia1, name="shownotisia1"),
  
    path('kontaktu/', views_kontaktu.inputokontaktu, name="inputokontaktu"),
    path('lista/kontaktu/', views_kontaktu.listakontaktu, name="listakontaktu"),
    path('hamos/kontaktu/<int:id>/', views_kontaktu.hamoskontaktu, name="hamoskontaktu"),

    #reviewona notisia artigu
    path('reviewona/<str:id>',views_noti.reviewona, name="reviewona"),
    path('publika/<str:id>',views_noti.publika, name="publika"),
    path('kansela/<str:id>',views_noti.kansela, name="kansela"),
  
    #atualiza
    path('atualiza/noti/<str:id>/',views_noti.updatenoti, name="updatenoti"),
    path('hamos/noti/<int:id>/',views_noti.hamosnoti, name="hamosnoti"),
    path('detailnotisia/noti/<str:id>/',views_noti.detailnotisia, name="detailnotisia"),

    #Galeria
    path('galeria/', views_galeria.galeria, name="galeria"),
    path('galeria/input/', views_galeria.inputgaleria, name="inputgaleria"),
    path('galeria/update/<str:id>', views_galeria.updategaleria, name="updategaleria"),
    path('galeria/hamos/<int:id>', views_galeria.hamosgaleria, name="hamosgaleria"),
    path('galeria/show/', views_galeria.show, name="showgaleria"),
    path('showcover/galeria/', views_galeria.showcover, name="showcover"),
    
    #foto video
    path('foto/<int:galeria_id>', views_foto.foto, name="foto"),
    path('foto/input/<int:galeria_id>', views_foto.inputfoto, name="inputfoto"),
    path('foto/update/<str:id>', views_foto.updatefoto, name="updatefoto"),
    path('foto/hamos/<int:id>', views_foto.hamosfoto, name="hamosfoto"),
    path('foto/detailufoto/<int:galeria_id>',views_foto.detailufoto, name="detailufoto"),
   
    #Video showvideo
     path('video/', views_video.video, name="video"),
     path('video/input/', views_video.inputvideo, name="inputvideo"),
     path('video/update/<int:id>', views_video.updatevideo, name="updatevideo"),
     path('video/hamos/<int:id>', views_video.hamosvideo, name="hamosvideo"),
     path('video/show/', views_video.show, name="showvideo"),
     path('showvideo/video/', views_video.showvideo, name="showvideo1"),

    #Kategoria showcover atividade download-registumenbrokmbo-excel/
    path('lista/artigu/', views_artigu.listaartigu, name="listaartigu"),
    path('input/artigu/', views_artigu.inputartigu, name="inputartigu"),
    path('atualiza/artigu/<str:id>/', views_artigu.updateartigu, name="updateartigu"),
    path('hamos/artigu/<int:id>/',views_artigu.hamosartigu, name="hamosartigu"),
    path('showartigu/artigu/', views_artigu.showartigu, name="showartigu"),

    path('publikasaunkmbo/download_qr_code/<str:id>/', views_publikasaunkmbo.download_qr_code, name='download_qr_code'),




    
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)