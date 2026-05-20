<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>La Buse - Assistant intelligent pour les droits du travail</title>
    <!-- Tailwind CSS pour un design moderne, épuré et réactif -->
    <script src="https://cdn.tailwindcss.com"></script>
    <!-- Chart.js pour des visualisations de salaires et primes -->
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
    <style>
        body {
            font-family: 'Inter', sans-serif;
            background-color: #F4F5FC;
            color: #1E203B;
            overflow-x: hidden;
        }
        .chart-container {
            position: relative;
            width: 100%;
            max-width: 600px;
            margin-left: auto;
            margin-right: auto;
            height: 250px;
            max-height: 300px;
        }
        /* Style personnalisé pour les cartes épurées de la maquette (Photo 2) */
        .maquette-card {
            background-color: #FFFFFF;
            border-radius: 20px;
            border: 1px solid rgba(0, 0, 0, 0.05);
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.01);
            transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
        }
        .maquette-card:hover {
            transform: translateY(-4px) scale(1.01);
            box-shadow: 0 12px 30px rgba(85, 81, 255, 0.1);
            border-color: rgba(85, 81, 255, 0.25);
        }
        /* Mode Contraste Élevé */
        .high-contrast {
            background-color: #000000 !important;
            color: #FFFFFF !important;
        }
        .high-contrast .maquette-card {
            background-color: #111111 !important;
            border-color: #FFFF00 !important;
            color: #FFFFFF !important;
        }
        .high-contrast h1, .high-contrast h2, .high-contrast h3, .high-contrast p, .high-contrast span {
            color: #FFFFFF !important;
        }
        .high-contrast button, .high-contrast .st-btn-act {
            background-color: #FFFF00 !important;
            color: #000000 !important;
            border: 2px solid #FFFFFF !important;
        }
        /* Cacher la scrollbar */
        .no-scrollbar::-webkit-scrollbar {
            display: none;
        }
        .no-scrollbar {
            -ms-overflow-style: none;
            scrollbar-width: none;
        }
        /* Chouette logo hover effects */
        .chouette-logo {
            transition: transform 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        }
        .chouette-logo:hover {
            transform: rotate(5deg) scale(1.05);
        }
        /* Effet moderne de lueur sur boutons */
        .btn-glow {
            box-shadow: 0 4px 14px rgba(85, 81, 255, 0.3);
            transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
        }
        .btn-glow:hover {
            box-shadow: 0 6px 20px rgba(85, 81, 255, 0.5);
            transform: translateY(-2px) scale(1.02);
        }
        .btn-glow:active {
            transform: translateY(1px) scale(0.98);
        }
    </style>
</head>
<body class="flex min-h-screen bg-[#F4F5FC] transition-colors duration-200">

    <!-- ================= ÉCRAN D'ACCÈS SÉCURISÉ (PIN) ================= -->
    <div id="pin-screen" class="fixed inset-0 bg-[#F4F5FC] z-50 flex flex-col items-center justify-center p-4 animate-fade-in">
        <!-- Logo chouette Photo 2 -->
        <div style="width: 140px; height: 140px; background: radial-gradient(circle, #E8E7FF 0%, #C3BFFF 100%); border-radius: 50%; position: relative; box-shadow: 0 10px 30px rgba(85, 81, 255, 0.25); display: flex; align-items: center; justify-content: center; margin-bottom: 25px;" class="chouette-logo">
            <div style="position: absolute; top: 12px; left: 28px; width: 0; height: 0; border-left: 18px solid transparent; border-right: 18px solid transparent; border-bottom: 35px solid #5551FF; transform: rotate(-18deg);"></div>
            <div style="position: absolute; top: 12px; right: 28px; width: 0; height: 0; border-left: 18px solid transparent; border-right: 18px solid transparent; border-bottom: 35px solid #5551FF; transform: rotate(18deg);"></div>
            <div style="width: 90px; height: 105px; background-color: #5551FF; border-radius: 50% 50% 45% 45%; position: relative; overflow: hidden; display: flex; align-items: center; justify-content: center;">
                <div style="position: absolute; bottom: -8px; width: 70px; height: 70px; background-color: #F4F5FC; border-radius: 50%;"></div>
            </div>
            <div style="position: absolute; top: 40px; left: 32px; width: 38px; height: 38px; background-color: #FFFFFF; border-radius: 50%; display: flex; align-items: center; justify-content: center; box-shadow: inset 0 2px 5px rgba(0,0,0,0.15);">
                <div style="width: 22px; height: 22px; background-color: #574B3C; border-radius: 50%; position: relative;">
                    <div style="width: 12px; height: 12px; background-color: #1E203B; border-radius: 50%;">
                        <div style="width: 5px; height: 5px; background-color: #FFFFFF; border-radius: 50%; position: absolute; top: 2px; left: 2px;"></div>
                    </div>
                </div>
            </div>
            <div style="position: absolute; top: 40px; right: 32px; width: 38px; height: 38px; background-color: #FFFFFF; border-radius: 50%; display: flex; align-items: center; justify-content: center; box-shadow: inset 0 2px 5px rgba(0,0,0,0.15);">
                <div style="width: 22px; height: 22px; background-color: #574B3C; border-radius: 50%; position: relative;">
                    <div style="width: 12px; height: 12px; background-color: #1E203B; border-radius: 50%;">
                        <div style="width: 5px; height: 5px; background-color: #FFFFFF; border-radius: 50%; position: absolute; top: 2px; left: 2px;"></div>
                    </div>
                </div>
            </div>
            <div style="position: absolute; top: 68px; width: 0; height: 0; border-left: 9px solid transparent; border-right: 9px solid transparent; border-top: 15px solid #FF9F43; z-index: 10;"></div>
        </div>
        <div class="bg-white p-8 rounded-3xl border border-gray-100 shadow-xl w-full max-w-sm text-center">
            <h2 class="text-2xl font-extrabold text-[#1E203B] mb-2">Accès sécurisé</h2>
            <p class="text-xs text-gray-400 mb-6">Saisissez votre code PIN pour accéder à la plateforme d'audit</p>
            <input type="password" id="pin-input" maxlength="4" placeholder="••••" class="w-full text-center bg-[#F4F5FC] border border-transparent rounded-2xl py-4 text-2xl tracking-widest outline-none focus:border-[#5551FF] focus:bg-white transition-all mb-4">
            <button onclick="unlockApp()" class="w-full bg-[#5551FF] text-white py-4 rounded-2xl font-bold hover:bg-[#413CFF] transition-all duration-300 transform active:scale-95 shadow-md hover:shadow-lg hover:shadow-[#5551FF]/20">Déverrouiller</button>
            <p id="pin-error" class="text-xs text-red-500 font-semibold mt-3 hidden animate-shake">Code PIN incorrect. Veuillez réessayer.</p>
        </div>
    </div>

    <!-- ================= BARRE LATÉRALE GAUCHE (MENU & ACCESSIBILITÉ) ================= -->
    <aside id="sidebar" class="w-64 bg-white border-r border-gray-100 flex flex-col shrink-0 z-20 hidden">
        <div class="p-6 border-b border-gray-100 flex items-center gap-3">
            <div class="w-11 h-11 rounded-full bg-[#E8E7FF] flex items-center justify-center relative shadow-sm shrink-0 chouette-logo cursor-pointer">
                <div class="w-2.5 h-2.5 bg-[#5551FF] rounded-full absolute top-3.5 left-2.5"></div>
                <div class="w-2.5 h-2.5 bg-[#5551FF] rounded-full absolute top-3.5 right-2.5"></div>
                <div class="w-0 h-0 border-l-[5px] border-l-transparent border-r-[5px] border-r-transparent border-top-[7px] border-top-[#FF9F43] absolute bottom-3.5"></div>
            </div>
            <div>
                <h1 class="text-xl font-extrabold text-[#1E203B] tracking-tight" data-tts="La buse">la buse</h1>
                <span class="text-xs text-[#5551FF] font-bold">Abonnement Actif</span>
            </div>
        </div>

        <nav class="flex-1 p-4 space-y-1 overflow-y-auto no-scrollbar">
            <button onclick="switchView('Accueil')" id="btn-menu-Accueil" class="w-full flex items-center gap-3 px-4 py-3 rounded-xl text-left font-semibold text-[#5551FF] bg-[#5551FF]/10 transition-all duration-300 transform active:scale-95 hover:bg-[#5551FF]/20" data-tts="Onglet Accueil">
                <span>🏠</span> Accueil
            </button>
            <button onclick="switchView('Sentinelles')" id="btn-menu-Sentinelles" class="w-full flex items-center gap-3 px-4 py-3 rounded-xl text-left font-semibold text-gray-600 hover:bg-gray-50 transition-all duration-300 transform active:scale-95" data-tts="Onglet Réseau Sentinelles">
                <span>🛡️</span> Réseau Sentinelles
            </button>
            <button onclick="switchView('Primes')" id="btn-menu-Primes" class="w-full flex items-center gap-3 px-4 py-3 rounded-xl text-left font-semibold text-gray-600 hover:bg-gray-50 transition-all duration-300 transform active:scale-95" data-tts="Onglet Calculateur de primes">
                <span>💎</span> Calculateur de primes
            </button>
        </nav>

        <div class="p-4 border-t border-gray-100 space-y-4">
            <h4 class="text-xs font-bold text-gray-400 uppercase tracking-wider">Configuration</h4>
            
            <div class="space-y-3 text-sm text-gray-700">
                <div class="flex justify-between items-center">
                    <span class="text-xs font-semibold">♿ Mode non voyant</span>
                    <input type="checkbox" id="chk-non-voyant" onchange="toggleNonVoyant(this)" class="accent-[#5551FF] w-4 h-4 cursor-pointer">
                </div>

                <div class="flex justify-between items-center">
                    <span class="text-xs font-semibold">🔊 Audio au survol</span>
                    <input type="checkbox" id="chk-audio-hover" onchange="toggleAudioHover(this)" class="accent-[#5551FF] w-4 h-4 cursor-pointer">
                </div>

                <div class="flex justify-between items-center">
                    <span class="text-xs font-semibold">🌓 Contraste élevé</span>
                    <input type="checkbox" id="chk-contrast" onchange="toggleContrast(this)" class="accent-[#5551FF] w-4 h-4 cursor-pointer">
                </div>
                
                <div class="flex justify-between items-center">
                    <span class="text-xs font-semibold">📝 Transcription</span>
                    <input type="checkbox" id="chk-transcription" onchange="toggleTranscription(this)" class="accent-[#5551FF] w-4 h-4 cursor-pointer">
                </div>
            </div>

            <button onclick="resetAccessibility()" class="w-full bg-gray-100 hover:bg-gray-200 text-gray-700 font-semibold py-2 rounded-xl text-xs transition-all duration-300 transform active:scale-95">
                Mode Normal (Normal)
            </button>
        </div>
    </aside>

    <!-- ================= CONTENUR DE PAGE ASYMÉTRIQUE ================= -->
    <div id="main-content-layout" class="flex-1 flex flex-col min-w-0 overflow-hidden hidden animate-fade-in">
        
        <!-- En-tête Global de Recherche & Profil -->
        <header class="h-20 bg-white border-b border-gray-100 flex items-center justify-between px-8 shrink-0 z-10">
            <div class="w-96 relative">
                <input type="text" id="global-search" placeholder="Rechercher un sujet, une question..." class="w-full bg-[#F4F5FC] border border-transparent rounded-xl py-2.5 pl-10 pr-4 text-sm outline-none focus:border-[#5551FF] focus:bg-white transition-all">
                <span class="absolute left-3.5 top-3.5 text-gray-400 text-sm">🔍</span>
            </div>
            
            <div class="flex items-center gap-6">
                <button onclick="switchView('Sentinelles')" class="bg-[#5551FF] text-white px-4 py-2 rounded-xl text-sm font-semibold hover:bg-[#413CFF] transition-all duration-300 transform active:scale-95 shadow-sm hover:shadow-lg hover:shadow-[#5551FF]/20" data-tts="Saisir un expert">Saisir un expert</button>
                <div class="w-px h-6 bg-gray-200"></div>
                <div class="flex items-center gap-3">
                    <div class="w-10 h-10 rounded-full bg-[#5551FF] text-white flex items-center justify-center font-bold shadow-md">A</div>
                    <div>
                        <span class="text-xs text-gray-400 block font-medium">Bienvenue</span>
                        <strong class="text-sm text-[#1E203B] block font-bold">Alexandre</strong>
                    </div>
                </div>
            </div>
        </header>

        <!-- Zone de Défilement Principale -->
        <div class="flex-1 flex overflow-hidden">
            
            <!-- CONTENU CENTRAL LARGE -->
            <div class="flex-1 p-8 overflow-y-auto no-scrollbar">
                
                <!-- ================= VUE : ACCUEIL ================= -->
                <section id="view-Accueil" class="view-section space-y-8 animate-fade-in">
                    <!-- Section Titre Maquette -->
                    <div class="flex flex-col md:flex-row items-center justify-between gap-8 bg-white p-8 rounded-3xl border border-gray-100 relative overflow-hidden">
                        <div class="space-y-4 max-w-xl z-10">
                            <h2 class="text-4xl font-extrabold text-[#1E203B] leading-tight animate-slide-up" data-tts="La buse, votre moteur de recherche au service du monde du travail.">
                                La buse, votre moteur <br>de recherche au service <br><span class="text-[#5551FF]">du monde du travail.</span>
                            </h2>
                            <p class="text-gray-500 text-base" data-tts="Posez vos questions, vérifiez vos primes et passez à l'action.">Posez vos questions, vérifiez vos primes et passez à l'action.</p>
                        </div>
                        
                        <!-- Mascotte Chouette Ronde de la Photo 2 -->
                        <div class="shrink-0 z-10">
                            <div style="width: 150px; height: 150px; background: radial-gradient(circle, #E8E7FF 0%, #C3BFFF 100%); border-radius: 50%; position: relative; box-shadow: 0 10px 30px rgba(85, 81, 255, 0.25); display: flex; align-items: center; justify-content: center;" class="chouette-logo cursor-pointer">
                                <div style="position: absolute; top: 12px; left: 28px; width: 0; height: 0; border-left: 18px solid transparent; border-right: 18px solid transparent; border-bottom: 35px solid #5551FF; transform: rotate(-18deg);"></div>
                                <div style="position: absolute; top: 12px; right: 28px; width: 0; height: 0; border-left: 18px solid transparent; border-right: 18px solid transparent; border-bottom: 35px solid #5551FF; transform: rotate(18deg);"></div>
                                <div style="width: 90px; height: 105px; background-color: #5551FF; border-radius: 50% 50% 45% 45%; position: relative; overflow: hidden; display: flex; align-items: center; justify-content: center;">
                                    <div style="position: absolute; bottom: -8px; width: 70px; height: 70px; background-color: #F4F5FC; border-radius: 50%;"></div>
                                </div>
                                <div style="position: absolute; top: 40px; left: 32px; width: 38px; height: 38px; background-color: #FFFFFF; border-radius: 50%; display: flex; align-items: center; justify-content: center; box-shadow: inset 0 2px 5px rgba(0,0,0,0.15);">
                                    <div style="width: 22px; height: 22px; background-color: #574B3C; border-radius: 50%; position: relative;">
                                        <div style="width: 12px; height: 12px; background-color: #1E203B; border-radius: 50%;">
                                            <div style="width: 5px; height: 5px; background-color: #FFFFFF; border-radius: 50%; position: absolute; top: 2px; left: 2px;"></div>
                                        </div>
                                    </div>
                                </div>
                                <div style="position: absolute; top: 40px; right: 32px; width: 38px; height: 38px; background-color: #FFFFFF; border-radius: 50%; display: flex; align-items: center; justify-content: center; box-shadow: inset 0 2px 5px rgba(0,0,0,0.15);">
                                    <div style="width: 22px; height: 22px; background-color: #574B3C; border-radius: 50%; position: relative;">
                                        <div style="width: 12px; height: 12px; background-color: #1E203B; border-radius: 50%;">
                                            <div style="width: 5px; height: 5px; background-color: #FFFFFF; border-radius: 50%; position: absolute; top: 2px; left: 2px;"></div>
                                        </div>
                                    </div>
                                </div>
                                <div style="position: absolute; top: 68px; width: 0; height: 0; border-left: 9px solid transparent; border-right: 9px solid transparent; border-top: 15px solid #FF9F43; z-index: 10;"></div>
                            </div>
                        </div>
                    </div>

                    <!-- ================= FUSION : EAGLE AGENT & AUDIT DOCUMENTAIRE MULTI-FICHIERS ================= -->
                    <div class="maquette-card p-6 space-y-6">
                        <div class="flex items-center gap-3">
                            <span class="text-4xl transition-transform duration-300 hover:rotate-12 cursor-pointer">🦅</span>
                            <div>
                                <h3 class="text-lg font-bold text-[#1E203B]">Eagle Agent IA — Assistant de Recherche & Audit de Documents</h3>
                                <p class="text-xs text-gray-500">Posez vos questions juridiques ou déposez vos pièces pour une analyse croisée immédiate (Légifrance & Juritravail).</p>
                            </div>
                        </div>

                        <!-- Dropzone d'importation multi-documents -->
                        <div class="border-2 border-dashed border-gray-200 hover:border-[#5551FF] rounded-2xl p-6 text-center transition-all duration-300 relative bg-gray-50/50 hover:bg-[#5551FF]/5">
                            <input type="file" id="multi-doc-uploader" multiple onchange="handleMultiFileUpload()" class="absolute inset-0 w-full h-full opacity-0 cursor-pointer">
                            <span class="text-4xl block mb-2">📂</span>
                            <strong class="text-sm text-[#1E203B] block">Glissez vos pièces ici ou cliquez pour parcourir</strong>
                            <span class="text-xs text-gray-400 mt-1 block">Fiches de paie, Contrats, Avenants, CV (PDF, PNG, JPG)</span>
                        </div>

                        <!-- Liste dynamique des documents importés -->
                        <div id="uploaded-files-container" class="hidden flex flex-wrap gap-2 pt-2">
                            <!-- Généré via JS -->
                        </div>

                        <!-- Formulaire de question d'accueil -->
                        <div class="space-y-4">
                            <div class="flex gap-3">
                                <input type="text" id="home-search-input" placeholder="Posez votre question réglementaire ou demandez un audit (Ex: Mon contrat est-il conforme ?)..." class="flex-1 bg-white border border-gray-200 rounded-2xl px-5 py-4 text-sm outline-none focus:border-[#5551FF] transition-all shadow-sm">
                                <button onclick="triggerHomeGrokSearch()" class="bg-[#5551FF] text-white px-8 py-4 rounded-2xl font-bold btn-glow shrink-0 shadow-lg">Lancer l'audit</button>
                            </div>
                            
                            <!-- Zone d'animation de chargement sémantique Grok AI -->
                            <div id="grok-loader" class="hidden maquette-card p-6 border border-[#5551FF]/20 bg-[#5551FF]/5 space-y-3">
                                <div class="flex items-center gap-3">
                                    <span class="animate-spin text-xl">⚡</span>
                                    <strong class="text-sm text-[#5551FF]" id="grok-loader-step">Initialisation du moteur de recherche Grok AI...</strong>
                                </div>
                            </div>

                            <!-- Affichage de la réponse directly en dessous de la recherche -->
                            <div id="home-answer-card" class="hidden maquette-card p-6 border-2 border-[#5551FF] bg-[#5551FF]/5 space-y-4">
                                <div class="flex justify-between items-start">
                                    <h4 class="font-bold text-lg text-[#1E203B]">Rapport d'analyse de conformité (Juritravail & Légifrance)</h4>
                                    <button onclick="hideHomeAnswer()" class="text-gray-400 hover:text-gray-600 text-xs font-semibold">Masquer ✖</button>
                                </div>
                                <p id="home-answer-text" class="text-sm text-gray-800 leading-relaxed"></p>
                                <div class="flex gap-3 items-center">
                                    <button id="btn-listen-home-answer" class="bg-[#5551FF] text-white font-semibold px-4 py-2 rounded-xl text-xs hover:bg-[#413CFF] transition-all duration-300 transform active:scale-95">🔊 Écouter la réponse</button>
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- Suggestions Rapides d'Accueil -->
                    <div class="space-y-2">
                        <span class="text-xs font-bold text-gray-400 uppercase tracking-wider">Suggestions rapides</span>
                        <div class="flex flex-wrap gap-2">
                            <button onclick="setHomeQuery('Puis-je refuser des heures supplémentaires ?')" class="bg-white border border-gray-200 hover:border-[#5551FF] text-xs font-medium text-gray-700 px-4 py-2.5 rounded-xl transition-all">Puis-je refuser des heures supplémentaires ?</button>
                            <button onclick="setHomeQuery('Quelles sont mes indemnités en cas de licenciement ?')" class="bg-white border border-gray-200 hover:border-[#5551FF] text-xs font-medium text-gray-700 px-4 py-2.5 rounded-xl transition-all">Quelles sont mes indemnités en cas de licenciement ?</button>
                            <button onclick="setHomeQuery('Mon employeur peut-il modifier mon contrat ?')" class="bg-white border border-gray-200 hover:border-[#5551FF] text-xs font-medium text-gray-700 px-4 py-2.5 rounded-xl transition-all">Mon employeur peut-il modifier mon contrat ?</button>
                        </div>
                    </div>

                    <!-- Carrousel d'Informations interactif et dynamique -->
                    <div class="carousel-container maquette-card">
                        <span id="carousel-badge" class="carousel-badge" data-tts="Prévention">Prévention RPS</span>
                        <h3 id="carousel-title" class="carousel-title" data-tts="Votre santé est une priorité absolue">🛡️ Votre santé est une priorité absolue</h3>
                        <p id="carousel-desc" class="carousel-desc" data-tts="L'employeur est légalement tenu de protéger votre santé physique et mentale (Article L4121-1 du Code du travail).">L'employeur est légalement tenu de protéger votre santé physique et mentale (Article L4121-1 du Code du travail).</p>
                        
                        <div class="flex items-center gap-3">
                            <button onclick="prevCarousel()" class="bg-[#F4F5FC] hover:bg-[#E8E7FF] text-[#5551FF] font-semibold px-4 py-2 rounded-xl text-xs transition-all duration-300 transform active:scale-95">⬅️ Précédent</button>
                            <button onclick="nextCarousel()" class="bg-[#F4F5FC] hover:bg-[#E8E7FF] text-[#5551FF] font-semibold px-4 py-2 rounded-xl text-xs transition-all duration-300 transform active:scale-95">Suivant ➡️</button>
                        </div>
                    </div>

                    <!-- Grille Actions (Ce que La buse peut faire pour vous) -->
                    <div class="space-y-4">
                        <h3 class="text-xl font-bold text-[#1E203B]" data-tts="Ce que la buse peut faire pour vous">Ce que La buse peut faire pour vous</h3>
                        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                            <div onclick="switchView('Accueil')" class="maquette-card p-6 cursor-pointer flex gap-4 items-start" data-tts="Dalle Eagle Agent.">
                                <span class="text-3xl transition-transform duration-300 hover:rotate-12">🦅</span>
                                <div>
                                    <h4 class="font-bold text-lg text-[#1E203B]">Eagle Agent IA & Audit</h4>
                                    <p class="text-sm text-gray-500 mt-1">Posez vos questions et importez vos pièces d'audit (CV, contrats, fiches de paie) pour déceler des anomalies de salaire.</p>
                                </div>
                            </div>
                            <div onclick="switchView('Sentinelles')" class="maquette-card p-6 cursor-pointer flex gap-4 items-start" data-tts="Dalle Réseau Sentinelles.">
                                <span class="text-3xl transition-transform duration-300 hover:rotate-12">🛡</span>
                                <div>
                                    <h4 class="font-bold text-lg text-[#1E203B]">Réseau Sentinelles</h4>
                                    <p class="text-sm text-gray-500 mt-1">Soyez mis en relation avec des délégués syndicaux ou des avocats spécialistes de proximité.</p>
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- Bannière d'Action Premium (Photo 2) -->
                    <div class="bg-gradient-to-r from-[#5551FF] to-[#413CFF] text-white p-8 rounded-3xl flex flex-col md:flex-row items-center justify-between gap-6" data-tts="Vos droits. Notre mission.">
                        <div class="space-y-2">
                            <h3 class="text-xl font-bold">Vos droits. Notre mission.</h3>
                            <p class="text-sm text-blue-100">La buse vous aide à comprendre, vérifier et défendre vos droits au travail en toute sécurité.</p>
                        </div>
                        <button onclick="switchView('Sentinelles')" class="bg-white text-[#5551FF] font-semibold px-6 py-3 rounded-xl shadow-sm hover:bg-gray-50 transition-all duration-300 transform active:scale-95 shrink-0">Contacter un expert</button>
                    </div>

                    <!-- Colonnes de réassurance de la Photo 2 -->
                    <div class="grid grid-cols-2 md:grid-cols-4 gap-6 pt-4">
                        <div class="text-center" data-tts="Fiable & sourcé">
                            <span class="text-2xl block mb-2 transition-transform duration-300 hover:scale-110 cursor-pointer">🛡️</span>
                            <strong class="text-xs font-bold text-gray-700 block">Fiable & sourcé</strong>
                            <span class="text-[10px] text-gray-400">Bases sur la loi</span>
                        </div>
                        <div class="text-center" data-tts="Confidentiel">
                            <span class="text-2xl block mb-2 transition-transform duration-300 hover:scale-110 cursor-pointer">🔒</span>
                            <strong class="text-xs font-bold text-gray-700 block">Confidentiel</strong>
                            <span class="text-[10px] text-gray-400">Données protégées</span>
                        </div>
                        <div class="text-center" data-tts="À jour">
                            <span class="text-2xl block mb-2 transition-transform duration-300 hover:scale-110 cursor-pointer">📅</span>
                            <strong class="text-xs font-bold text-gray-700 block">À jour</strong>
                            <span class="text-[10px] text-gray-400">Mises à jour régulières</span>
                        </div>
                        <div class="text-center" data-tts="Accessible à tous">
                            <span class="text-2xl block mb-2 transition-transform duration-300 hover:scale-110 cursor-pointer">👥</span>
                            <strong class="text-xs font-bold text-gray-700 block">Accessible à tous</strong>
                            <span class="text-[10px] text-gray-400">Zéro barrière</span>
                        </div>
                    </div>
                </section>

                <!-- ================= VUE : SENTINELLES ================= -->
                <section id="view-Sentinelles" class="view-section hidden space-y-6">
                    <div class="mb-4">
                        <h2 class="text-3xl font-bold text-[#1E203B] mb-2" data-tts="Réseau des sentinelles et experts de proximité">🛡️ Réseau Sentinelles</h2>
                        <p class="text-gray-500 text-sm">Recherchez un avocat ou un délégué spécialiste en droit social à proximité de Niort / Saint-Maxire (79).</p>
                    </div>

                    <!-- Bouton Pop-up de Localisation Navigateur -->
                    <div class="flex flex-col md:flex-row gap-4 items-center justify-between bg-white p-4 rounded-2xl border border-gray-100 shadow-sm">
                        <div>
                            <strong class="text-sm text-[#1E203B] block">📍 Optimisez votre réseau par géolocalisation</strong>
                            <span class="text-xs text-gray-400">Demande l'accès GPS du navigateur pour calculer les distances réelles de nos services.</span>
                        </div>
                        <button onclick="requestHTML5Location()" class="bg-[#5551FF] text-white px-5 py-2.5 rounded-xl text-xs font-bold hover:bg-[#413CFF] transition-all shrink-0 duration-300 transform active:scale-95 shadow-md">Autoriser la localisation</button>
                    </div>

                    <div class="flex gap-4">
                        <input type="text" id="sentinel-filter" onkeyup="filterSentinelles()" placeholder="Rechercher par avocat, syndicat, département (ex: 79)..." class="flex-1 bg-white border border-gray-200 rounded-xl px-4 py-3 text-sm outline-none focus:border-[#5551FF] transition-all shadow-sm">
                    </div>

                    <div id="sentinel-list" class="grid grid-cols-1 md:grid-cols-2 gap-6">
                        <!-- Rendu dynamique JS -->
                    </div>
                </section>

                <!-- ================= VUE : PRIMES ================= -->
                <section id="view-Primes" class="view-section hidden space-y-6">
                    <div class="mb-4">
                        <h2 class="text-3xl font-bold text-[#1E203B] mb-2" data-tts="Calculateurs de primes et de salaire">💎 Calculateurs Primes & Salaires</h2>
                        <p class="text-gray-500 text-sm">Estimez vos primes d'écart Infinity, votre salaire net et vos indemnités de maladie.</p>
                    </div>

                    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
                        <div class="space-y-6">
                            <!-- Calculateur Prime d'écart Infinity -->
                            <div class="maquette-card p-6 space-y-4">
                                <h3 class="text-lg font-bold text-[#1E203B] flex items-center gap-2"><span>📈</span> Prime d'écart Infinity</h3>
                                <div>
                                    <label class="block text-xs font-semibold text-gray-500 uppercase mb-1">Chiffre d'Affaire Réalisé Magasin (€)</label>
                                    <input type="number" id="calc-ca" value="1850" oninput="updatePrimesAndSalaries()" class="w-full bg-[#F4F5FC] border border-transparent rounded-xl px-4 py-2.5 text-sm outline-none focus:border-[#5551FF] focus:bg-white transition-all">
                                </div>
                                <div>
                                    <label class="block text-xs font-semibold text-gray-500 uppercase mb-1">Heures Travaillées dans le Mois</label>
                                    <input type="number" id="calc-hours" value="48" oninput="updatePrimesAndSalaries()" class="w-full bg-[#F4F5FC] border border-transparent rounded-xl px-4 py-2.5 text-sm outline-none focus:border-[#5551FF] focus:bg-white transition-all">
                                </div>
                                <div class="bg-blue-50 p-4 rounded-xl border border-blue-100 flex justify-between items-center">
                                    <div>
                                        <span class="text-xs text-blue-500 block">Prime estimée :</span>
                                        <strong id="out-bonus" class="text-2xl font-bold text-[#5551FF]">0%</strong>
                                    </div>
                                    <span id="out-ecart" class="text-xs text-blue-600 font-semibold">Écart: 550.00 €</span>
                                </div>
                            </div>

                            <!-- Simulateur Salaire Brut -> Net & IJ -->
                            <div class="maquette-card p-6 space-y-4">
                                <h3 class="text-lg font-bold text-[#1E203B] flex items-center gap-2"><span>💰</span> Simulateur de Salaire</h3>
                                <div>
                                    <label class="block text-xs font-semibold text-gray-500 uppercase mb-1">Salaire Brut Mensuel (€)</label>
                                    <input type="number" id="calc-brut" value="2100" oninput="updatePrimesAndSalaries()" class="w-full bg-[#F4F5FC] border border-transparent rounded-xl px-4 py-2.5 text-sm outline-none focus:border-[#5551FF] focus:bg-white transition-all">
                                </div>
                                <div>
                                    <label class="block text-xs font-semibold text-gray-500 uppercase mb-1">Statut</label>
                                    <select id="calc-status" onchange="updatePrimesAndSalaries()" class="w-full bg-[#F4F5FC] border border-transparent rounded-xl px-4 py-2.5 text-sm outline-none focus:border-[#5551FF] focus:bg-white transition-all">
                                        <option value="non-cadre">Non-Cadre (Charges 22%)</option>
                                        <option value="cadre">Cadre (Charges 25%)</option>
                                    </select>
                                </div>
                                <div class="grid grid-cols-2 gap-4">
                                    <div class="bg-gray-50 p-3 rounded-xl border border-gray-100">
                                        <span class="text-xs text-gray-500 block">Salaire Net</span>
                                        <strong id="out-net" class="text-base text-gray-800">1638.00 €</strong>
                                    </div>
                                    <div class="bg-gray-50 p-3 rounded-xl border border-gray-100">
                                        <span class="text-xs text-gray-500 block">Indemnité IJ / Jour</span>
                                        <strong id="out-ij" class="text-base text-gray-800">34.52 €</strong>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <!-- Graphiques Interactifs -->
                        <div class="space-y-6">
                            <div class="maquette-card p-6">
                                <h4 class="text-xs font-bold text-gray-500 uppercase mb-4 text-center">Visualisation du Seuil d'Écart</h4>
                                <div class="chart-container">
                                    <canvas id="chart-ca"></canvas>
                                </div>
                            </div>
                            <div class="maquette-card p-6">
                                <h4 class="text-xs font-bold text-gray-500 uppercase mb-4 text-center">Répartition Salaire Brut</h4>
                                <div class="chart-container" style="height: 200px;">
                                    <canvas id="chart-salary"></canvas>
                                </div>
                            </div>
                        </div>
                    </div>
                </section>

            </div>

            <!-- ================= PANNEAU DE DROITE (ACCÈS RAPIDE - PHOTO 2) ================= -->
            <aside class="w-80 bg-[#F4F5FC] border-l border-gray-100 p-6 space-y-6 hidden xl:block overflow-y-auto no-scrollbar">
                
                <!-- Outils Rapides -->
                <div class="space-y-3">
                    <h4 class="text-xs font-bold text-gray-400 uppercase tracking-wider">Outils rapides</h4>
                    <div class="bg-white p-4 rounded-2xl border border-gray-100 space-y-3 shadow-sm text-sm text-gray-700">
                        <div onclick="switchView('Accueil')" class="flex items-center gap-2 cursor-pointer hover:text-[#5551FF] transition-all"><span>📄</span> Analyser mes documents</div>
                        <div onclick="switchView('Accueil')" class="flex items-center gap-2 cursor-pointer hover:text-[#5551FF] transition-all"><span>⚖️</span> Poser une question IA</div>
                        <div onclick="switchView('Sentinelles')" class="flex items-center gap-2 cursor-pointer hover:text-[#5551FF] transition-all"><span>🔍</span> Consulter mes droits</div>
                        <div onclick="switchView('Primes')" class="flex items-center gap-2 cursor-pointer hover:text-[#5551FF] transition-all"><span>💎</span> Simuler une prime</div>
                    </div>
                </div>

                <!-- Section Aide Immédiate -->
                <div class="space-y-3">
                    <h4 class="text-xs font-bold text-gray-400 uppercase tracking-wider">Besoin d'aide immédiate ?</h4>
                    <div class="bg-[#E8E7FF]/40 p-4 rounded-2xl border border-[#5551FF]/10 text-sm space-y-4">
                        <p class="text-xs text-gray-500">Nos experts du réseau Sentinelles sont connectés et à votre écoute.</p>
                        <button onclick="switchView('Sentinelles')" class="w-full bg-[#5551FF] text-white py-2.5 rounded-xl text-xs font-bold hover:bg-[#413CFF] transition-all duration-300 transform active:scale-95 shadow-md">Être mis en relation</button>
                    </div>
                </div>

            </aside>

        </div>

    </div>

    <!-- Pied de page permanent avec Mentions Légales et Copyright (Photo 2) -->
    <footer id="main-footer" class="w-full bg-white border-t border-gray-100 py-6 px-8 z-10 text-center shrink-0 hidden">
        <div class="max-w-4xl mx-auto space-y-2 text-xs text-gray-400">
            <p class="font-bold text-gray-500">🦉 La Buse — Plateforme indépendante de surveillance salariale & d'audit</p>
            <p class="line-clamp-2 hover:line-clamp-none transition-all duration-300">
                <strong>Mentions Légales :</strong> Initiative privée indépendante de tout organisme étatique ou syndical. 
                Les analyses d'audit, de conformité et de primes sont délivrées à titre purement indicatif et s'appuient sur l'état du droit en vigueur et des bases de connaissances conventionnelles (Légifrance, Juritravail). Elles ne se substituent pas à un conseil juridique personnalisé.
            </p>
            <p class="font-semibold">
                Copyright © <span id="copyright-year"></span> — La Buse. Tous droits réservés.
            </p>
        </div>
    </footer>

    <!-- ================= CODE JAVASCRIPT GLOBAL ================= -->
    <script>
        // Base de données par défaut (en cas d'absence ou erreur de chargement experts_data.json)
        let EXPERT_DIRECTORY = [
            {"Type": "Avocat Spécialisé", "Nom": "Maître Lefebvre - Cabinet Droit du Travail Niort", "Contact": "05 49 24 88 99", "Email": "m.lefebvre@avocats-niort-travail.fr", "Adresse": "24 Rue de la Gare, 79000 Niort", "Departement": "79", "Region": "Nouvelle-Aquitaine", "lat": 46.3210, "lon": -0.4580, "Desc": "Expert reconnu en défense des salariés, contentieux prud'homal, requalification de contrats et harcèlement moral."},
            {"Type": "Avocat Spécialisé", "Nom": "Cabinet d'Avocats Droit du Travail Niortais", "Contact": "05 49 24 10 20", "Email": "secretariat@travail-niort-avocats.fr", "Adresse": "12 Rue de la Regratterie, 79000 Niort", "Departement": "79", "Region": "Nouvelle-Aquitaine", "lat": 46.3235, "lon": -0.4635, "Desc": "Spécialisé en licenciements individuels, collectifs, contrats de travail et Risques Psychosociaux (RPS)."},
            {"Type": "Avocat Spécialisé", "Nom": "Maître Claire Valois - Barreau des Deux-Sèvres", "Contact": "05 49 77 15 30", "Email": "c.valois@deux-sevres-avocats.fr", "Adresse": "45 Avenue de Limoges, 79000 Niort", "lat": 46.3190, "lon": -0.4480, "Desc": "Conseil et défense des salariés devant le Conseil de Prud'hommes de Niort."},
            {"Type": "Union Syndicale", "Nom": "UD CFDT Deux-Sèvres", "Contact": "05 49 24 51 32", "Email": "ud-79@cfdt.fr", "Adresse": "Maison des Syndicats, 79000 Niort", "Departement": "79", "Region": "Nouvelle-Aquitaine", "lat": 46.3280, "lon": -0.4610, "Desc": "Accompagnement syndical, permanence juridique et défense des droits des salariés du secteur privé."},
            {"Type": "Union Syndicale", "Nom": "Union Départementale CGT 79", "Contact": "05 49 24 35 12", "Email": "ud79@cgt.fr", "Adresse": "Place de la Comédie, 79000 Niort", "Departement": "79", "Region": "Nouvelle-Aquitaine", "lat": 46.3262, "lon": -0.4595, "Desc": "Permanences juridiques et défense collective face au harcèlement et à la pression au travail."},
            {"Type": "Défenseur des Droits", "Nom": "Point d'Accès au Droit - Maison de la Justice Niort", "Contact": "05 49 04 00 00", "Email": "pad-niort@justice.fr", "Adresse": "10 Rue du Tribunal, 79000 Niort", "Departement": "79", "Region": "Nouvelle-Aquitaine", "lat": 46.3242, "lon": -0.4645, "Desc": "Médiateur de proximité indépendant pour la défense de vos libertés individuelles au travail."}
        ];

        const CAROUSEL_ITEMS = [
            {"badge": "Prévention RPS", "titre": "🛡️ Votre santé est une priorité absolue", "description": "L'employeur est légalement tenu de protéger votre santé physique et mentale (Article L4121-1 du Code du travail)."},
            {"badge": "Primes & Salaires", "titre": "📈 Déplafonnement de prime Infinity V4", "description": "Atteignez les paliers de bonus de 20% à 100% en surveillant votre écart de CA magasin par rapport au seuil de référence de 1300 €."},
            {"badge": "Vos Droits", "titre": "⚖️ Droits & Prévoyance du Salarié", "description": "Bénéficiez de grilles de salaires garanties, de majorations pour heures de nuit et de garanties de prévoyance spécifiques."}
        ];

        // États de session locaux
        let sessionState = {
            carousel_index: 0,
            audio_on_hover: false,
            non_voyant: false,
            high_contrast: false,
            transcription: false,
            user_location: { lat: 46.3235, lon: -0.4635 }, // Niort par défaut
            ai_history: [],
            uploaded_files: []
        };

        let chartCaObj = null;
        let chartSalaryObj = null;

        // --- CONTRÔLE D'ACCÈS PIN CODE ---
        function unlockApp() {
            const pinVal = document.getElementById('pin-input').value;
            if (pinVal === '1234') {
                document.getElementById('pin-screen').classList.add('hidden');
                document.getElementById('sidebar').classList.remove('hidden');
                document.getElementById('main-content-layout').classList.remove('hidden');
                document.getElementById('main-footer').classList.remove('hidden');
                switchView('Accueil');
                toast("🔓 Accès déverrouillé avec succès !");
            } else {
                const err = document.getElementById('pin-error');
                err.classList.remove('hidden');
                document.getElementById('pin-input').value = "";
            }
        }

        // Écoute de la touche Entrée sur le champ de saisie du PIN
        document.getElementById('pin-input').addEventListener('keypress', function (e) {
            if (e.key === 'Enter') {
                unlockApp();
            }
        });

        // --- ROUTAGE DES ONGLES ---
        function switchView(viewId) {
            document.querySelectorAll('.view-section').forEach(sec => sec.classList.add('hidden'));
            const targetSection = document.getElementById('view-' + viewId);
            if(targetSection) targetSection.classList.remove('hidden');

            // Mise à jour de la classe CSS du bouton de menu actif
            document.querySelectorAll('aside nav button').forEach(btn => {
                btn.classList.remove('text-[#5551FF]', 'bg-[#5551FF]/10');
                btn.classList.add('text-gray-600', 'hover:bg-gray-50');
            });

            const activeBtn = document.getElementById('btn-menu-' + viewId);
            if(activeBtn) {
                activeBtn.classList.remove('text-gray-600', 'hover:bg-gray-50');
                activeBtn.classList.add('text-[#5551FF]', 'bg-[#5551FF]/10');
            }

            // Rafraîchir les visualisations au besoin
            if(viewId === 'Primes') {
                updatePrimesAndSalaries();
            } else if(viewId === 'Sentinelles') {
                renderSentinelles();
            }
        }

        // --- CONTRÔLES D'ACCESSIBILITÉ ---
        function toggleNonVoyant(cb) {
            sessionState.non_voyant = cb.checked;
            document.getElementById('chk-non-voyant').checked = cb.checked;
            document.body.style.fontSize = cb.checked ? "120%" : "100%";
        }

        function toggleAudioHover(cb) {
            sessionState.audio_on_hover = cb.checked;
            document.getElementById('chk-audio-hover').checked = cb.checked;
            toast(cb.checked ? "Audio au survol activé." : "Audio au survol coupé.");
        }

        function toggleContrast(cb) {
            sessionState.high_contrast = cb.checked;
            document.getElementById('chk-contrast').checked = cb.checked;
            if(cb.checked) {
                document.body.classList.add('high-contrast');
            } else {
                document.body.classList.remove('high-contrast');
            }
        }

        // --- SYNTHÈSE VOCALE SPEECH ---
        function speakText(text) {
            try {
                var synth = window.speechSynthesis || (window.parent && window.parent.speechSynthesis);
                if (synth) {
                    synth.cancel();
                    var utterance = new SpeechSynthesisUtterance(text);
                    utterance.lang = "fr-FR";
                    synth.speak(utterance);
                }
            } catch(e) {
                console.error("Synthese vocale inaccessible :", e);
            }
        }

        function toggleTranscription(cb) {
            sessionState.transcription = cb.checked;
            document.getElementById('chk-transcription').checked = cb.checked;
            toast(cb.checked ? "Transcription activée." : "Transcription coupée.");
        }

        function resetAccessibility() {
            sessionState.non_voyant = false;
            sessionState.audio_on_hover = false;
            sessionState.high_contrast = false;
            sessionState.transcription = false;
            
            document.getElementById('chk-non-voyant').checked = false;
            document.getElementById('chk-audio-hover').checked = false;
            document.getElementById('chk-contrast').checked = false;
            document.getElementById('chk-transcription').checked = false;
            
            document.body.style.fontSize = "100%";
            document.body.classList.remove('high-contrast');
            toast("Accessibilité réinitialisée.");
        }

        // --- CARROUSEL ACTU ---
        function nextCarousel() {
            sessionState.carousel_index = (sessionState.carousel_index + 1) % CAROUSEL_ITEMS.length;
            renderCarousel();
        }

        function prevCarousel() {
            sessionState.carousel_index = (sessionState.carousel_index - 1) % CAROUSEL_ITEMS.length;
            renderCarousel();
        }

        function renderCarousel() {
            const item = CAROUSEL_ITEMS[sessionState.carousel_index];
            document.getElementById('carousel-badge').innerText = item.badge;
            document.getElementById('carousel-badge').setAttribute('data-tts', item.badge);
            document.getElementById('carousel-title').innerText = item.titre;
            document.getElementById('carousel-title').setAttribute('data-tts', item.titre);
            document.getElementById('carousel-desc').innerText = item.description;
            document.getElementById('carousel-desc').setAttribute('data-tts', item.description);
        }

        // --- MODULE MULTI-DOCUMENTS D'EAGLE ---
        function handleMultiFileUpload() {
            const fileInput = document.getElementById('multi-doc-uploader');
            const container = document.getElementById('uploaded-files-container');
            container.innerHTML = "";
            sessionState.uploaded_files = [];

            if (fileInput.files.length > 0) {
                container.classList.remove('hidden');
                for (let i = 0; i < fileInput.files.length; i++) {
                    const file = fileInput.files[i];
                    sessionState.uploaded_files.push(file.name);
                    
                    // Rendu de badge individuel avec bouton de suppression
                    const badgeId = `uploaded-badge-${i}`;
                    container.innerHTML += `
                        <span id="${badgeId}" class="inline-flex items-center gap-1.5 bg-[#5551FF]/10 text-[#5551FF] font-bold text-xs px-3 py-1.5 rounded-full border border-[#5551FF]/20">
                            📄 ${file.name}
                            <button onclick="removeUploadedFile('${file.name}', '${badgeId}')" class="text-red-500 hover:text-red-700 ml-1 font-bold">✖</button>
                        </span>
                    `;
                }
                toast(`📎 ${fileInput.files.length} document(s) rattaché(s) à l'analyse sémantique.`);
            } else {
                container.classList.add('hidden');
            }
        }

        function removeUploadedFile(fileName, badgeId) {
            sessionState.uploaded_files = sessionState.uploaded_files.filter(f => f !== fileName);
            const badge = document.getElementById(badgeId);
            if (badge) {
                badge.remove();
            }
            if (sessionState.uploaded_files.length === 0) {
                document.getElementById('uploaded-files-container').classList.add('hidden');
            }
            toast(`🗑️ Document "${fileName}" retiré de l'analyse.`);
        }

        // --- RECHERCHE ET ANIMATION GROK AI (ACCUEIL) ---
        function setHomeQuery(query) {
            document.getElementById('home-search-input').value = query;
            triggerHomeGrokSearch();
        }

        function triggerHomeGrokSearch() {
            const query = document.getElementById('home-search-input').value.trim();
            if(!query) return;

            const loader = document.getElementById('grok-loader');
            const loaderStep = document.getElementById('grok-loader-step');
            const answerCard = document.getElementById('home-answer-card');

            answerCard.classList.add('hidden');
            loader.classList.remove('hidden');

            const steps = [
                "🔍 Exploration sémantique de la base de données Légifrance & Juritravail...",
                "⚖️ Interrogation des sources réglementaires & jurisprudences de branche...",
                "📊 Analyse comparative de vos pièces justificatives téléversées...",
                "⚡ Structuration de votre rapport d'analyse de conformité..."
            ];

            let stepIdx = 0;
            const interval = setInterval(() => {
                if(stepIdx < steps.length) {
                    loaderStep.innerText = steps[stepIdx];
                    stepIdx++;
                } else {
                    clearInterval(interval);
                    loader.classList.add('hidden');
                    
                    // Génération de la réponse Grok AI
                    const answer = call_eagle_ia_local(query, sessionState.uploaded_files);
                    sessionState.ai_history.push({ q: query, a: answer });

                    document.getElementById('home-answer-text').innerHTML = answer.replace(/\n/g, '<br>');
                    answerCard.classList.remove('hidden');

                    // Configuration du bouton d'écoute audio
                    document.getElementById('btn-listen-home-answer').onclick = function() {
                        speakText(answer);
                    };
                }
            }, 600);
        }

        function hideHomeAnswer() {
            document.getElementById('home-answer-card').classList.add('hidden');
        }

        // --- CONTEXT COGNITIF GROK AI AVEC JURITRAVAIL & MULTI-DOCS ---
        function call_eagle_ia_local(prompt, files = []) {
            const p_lower = prompt.toLowerCase();
            const intro = "⚡ **Grok (xAI) — Analyse sémantique Légale & Base Jurisprudence Juritravail**\n\n";
            let doc_context = "";

            if (files && files.length > 0) {
                doc_context = `ℹ️ **Documents analysés conjointement** : \`${files.join(', ')}\`\n`;
                doc_context += "- **Analyse de Pièces** : Détection des incohérences de salaires conventionnels, d'heures de nuit ou de classification de poste.\n\n";
            }

            if (p_lower.includes("harcèlement") || p_lower.includes("rps") || p_lower.includes("pression") || p_lower.includes("licenciement") || p_lower.includes("indemnit")) {
                if (p_lower.includes("licenciement") || p_lower.includes("indemnit")) {
                    return intro + doc_context + "### 📑 Analyse d'Indemnités de Licenciement (Code du Travail & Juritravail) :\n\n" +
                           "1. **Mode de calcul** : 1/4 de mois de salaire par année d'ancienneté pour les 10 premières années (Article R1234-2).\n" +
                           "2. **Calcul de l'indemnité conventionnelle** : Des clauses spécifiques s'appliquent sur vos primes récurrentes d'écart Infinity.\n\n" +
                           "### ⚠️ Anomalie détectée : \n" +
                           "Si vos pièces ne mentionnent pas l'intégration de vos variables de CA, vos calculs de primes de licenciement sont sous-évalués.";
                }
                return intro + doc_context + "### 🛡️ Risques Psychosociaux & Santé mentale (Article L4121-1) :\n" +
                       "L'employeur détient une obligation de sécurité de résultat quant à votre santé. L'absence d'enquête ou de mesures d'accompagnement directes est considérée comme un délit conventionnel majeur.\n\n" +
                       "### Recommandations de protection :\n" +
                       "Consignez par écrit les faits précis et notifiez immédiatement le médecin du travail de Niort.";
            } else if (p_lower.includes("heure") || p_lower.includes("planning") || p_lower.includes("délai")) {
                return intro + doc_context + "### ⚖️ Horaires & Délais de Prévenance (Juritravail) :\n" +
                       "- **Planning de garde/travail** : L'employeur doit vous notifier de tout changement au moins 7 jours à l'avance.\n" +
                       "- **Heures supplémentaires** : Majoration de 25% pour les 8 premières heures, et 50% au-delà.";
            } else {
                return intro + doc_context + "Analyse Grok complétée pour votre requête. Vos droits conventionnels imposent un repos quotidien de 11h consécutives et hebdomadaire de 35h consécutives.";
            }
        }

        // --- ACCÈS DE GÉOLOCALISATION SÉCURISÉE ---
        function requestHTML5Location() {
            if ("geolocation" in navigator) {
                navigator.geolocation.getCurrentPosition((pos) => {
                    sessionState.user_location.lat = pos.coords.latitude;
                    sessionState.user_location.lon = pos.coords.longitude;
                    toast("📍 Coordonnées récupérées avec succès !");
                    renderSentinelles();
                }, (err) => {
                    // Fallback : Demande manuelle de coordonnées / code postal en cas d'échec d'iframe
                    const manualPostal = prompt("📍 Entrez votre ville ou code postal à Niort (ex: 79000) pour trier les experts par proximité :");
                    if (manualPostal) {
                        toast(`📍 Position calibrée sur : ${manualPostal}`);
                        // Coordonnées approximatives de Niort pour le fallback
                        sessionState.user_location.lat = 46.3235;
                        sessionState.user_location.lon = -0.4635;
                        renderSentinelles();
                    }
                });
            }
        }

        // --- CALCUL DE DISTANCE HAVERSINE ---
        function haversine_distance(lat1, lon1, lat2, lon2) {
            const R = 6371.0;
            const dlat = (lat2 - lat1) * Math.PI / 180;
            const dlon = (lon2 - lon1) * Math.PI / 180;
            const a = Math.sin(dlat / 2) * Math.sin(dlat / 2) + Math.cos(lat1 * Math.PI / 180) * Math.cos(lat2 * Math.PI / 180) * Math.sin(dlon / 2) * Math.sin(dlon / 2);
            return R * 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
        }

        // --- RENDU ET EMAIL DES SENTINELLES ---
        function renderSentinelles(filter = "") {
            const container = document.getElementById('sentinel-list');
            container.innerHTML = "";

            const sorted = EXPERT_DIRECTORY.map(exp => {
                const dist = haversine_distance(sessionState.user_location.lat, sessionState.user_location.lon, exp.lat, exp.lon);
                return { ...exp, distance: dist };
            }).sort((a, b) => a.distance - b.distance);

            sorted.filter(exp => 
                exp.Nom.toLowerCase().includes(filter.toLowerCase()) || 
                exp.Adresse.toLowerCase().includes(filter.toLowerCase()) ||
                exp.Departement?.toLowerCase().includes(filter.toLowerCase())
            ).forEach((exp, idx) => {
                const badgeColor = exp.Type === "Avocat Spécialisé" ? "bg-purple-50 text-purple-700 border-purple-100" : "bg-yellow-50 text-yellow-700 border-yellow-100";
                
                container.innerHTML += `
                    <div class="maquette-card p-6 flex flex-col justify-between space-y-4">
                        <div class="space-y-2">
                            <div class="flex justify-between items-center">
                                <span class="px-2.5 py-1 text-xs font-bold border rounded-full ${badgeColor}">${exp.Type}</span>
                                <span class="text-xs text-[#5551FF] font-bold">📍 À ${exp.distance.toFixed(1)} km</span>
                            </div>
                            <h4 class="font-bold text-[#1E203B] text-lg">${exp.Nom}</h4>
                            <p class="text-xs text-gray-400">${exp.Adresse} ${exp.Departement ? '(Dép: ' + exp.Departement + ')' : ''}</p>
                            <p class="text-sm text-gray-600">${exp.Desc}</p>
                            
                            <label class="flex items-center gap-2 pt-2 cursor-pointer">
                                <input type="checkbox" id="chk-proof-${idx}" class="accent-[#5551FF]">
                                <span class="text-xs text-gray-500">Joindre mes preuves d'audit sémantique</span>
                            </label>
                        </div>
                        <div class="flex justify-between items-center border-t border-gray-50 pt-3">
                            <strong class="text-sm text-gray-800">📞 ${exp.Contact}</strong>
                            <button onclick="triggerDirectMail('${exp.Nom}', '${exp.Email}', ${idx})" class="bg-[#5551FF] hover:bg-[#413CFF] text-white text-xs font-bold px-4 py-2 rounded-xl transition-all duration-300 transform active:scale-95 shadow-md">
                                ✉saisir Saisir / Contacter
                            </button>
                        </div>
                    </div>
                `;
            });
        }

        function triggerDirectMail(name, email, idx) {
            const includeProofs = document.getElementById('chk-proof-' + idx).checked;
            const history = sessionState.ai_history;
            
            let lastQuery = "";
            let lastAnswer = "";
            if(history.length > 0) {
                lastQuery = history[history.length - 1].q;
                lastAnswer = history[history.length - 1].a;
            }

            const subject = "Demande d'accompagnement d'urgence - Alexandre via La Buse";
            let body = `Bonjour ${name},\n\n`;
            body += "Je vous sollicite en tant que Sentinelle afin d'obtenir vos conseils et d'évaluer l'opportunité d'une démarche d'accompagnement.\n\n";
            
            if(lastQuery) {
                body += `Mes échanges avec l'assistant de conformité Grok ont mis en lumière les éléments factuels suivants : "${lastQuery}"\n`;
            } else {
                body += "Situation exposée : Demande d'examen de conformité globale de mes bulletins de salaire et de mes primes contractuelles (Infinity V4).\n";
            }

            body += `\nStatut des preuves rattachées : ${includeProofs ? "Pièces d'audit jointes (bulletins de salaire, contrats)" : "Preuves à fournir lors de notre rendez-vous"}\n\n`;
            body += "Cordialement,\nAlexandre - Utilisateur Certifié La Buse";

            const mailtoUrl = `mailto:${email}?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`;
            window.open(mailtoUrl, '_blank');
        }

        function filterSentinelles() {
            const val = document.getElementById('sentinel-filter').value;
            renderSentinelles(val);
        }

        // --- CALCULATEUR DE PRÉLÈVEMENTS & CHARGES (CHART.JS) ---
        function initPrimesAndSalariesCharts() {
            const ctxCa = document.getElementById('chart-ca').getContext('2d');
            chartCaObj = new Chart(ctxCa, {
                type: 'bar',
                data: {
                    labels: ['Seuil 1300€', 'Seuil Prime', 'CA Réalisé'],
                    datasets: [{
                        data: [1300, 1711.69, 1850],
                        backgroundColor: ['#EBEBFF', '#D8D6FF', '#5551FF'],
                        borderRadius: 10
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: { legend: { display: false } }
                }
            });

            const ctxSal = document.getElementById('chart-salary').getContext('2d');
            chartSalaryObj = new Chart(ctxSal, {
                type: 'doughnut',
                data: {
                    labels: ['Salaire Net', 'Prélèvements/Charges'],
                    datasets: [{
                        data: [1638.00, 462.00],
                        backgroundColor: ['#5551FF', '#E8E7FF'],
                        borderWidth: 0
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    cutout: '75%',
                    plugins: { legend: { position: 'bottom' } }
                }
            });
        }

        function updatePrimesAndSalaries() {
            const ca = parseFloat(document.getElementById('calc-ca').value) || 0;
            const hours = parseFloat(document.getElementById('calc-hours').value) || 1;
            const brut = parseFloat(document.getElementById('calc-brut').value) || 0;
            const status = document.getElementById('calc-status').value;

            // Calcul primes
            const ecart = ca - 1300;
            let bonus = "0%";
            if(ecart >= 411.69) {
                const ratio = (ecart - 411.69) / hours;
                if(ratio >= 16) bonus = "100%";
                else if(ratio >= 13) bonus = "60%";
                else if(ratio >= 10) bonus = "40%";
                else if(ratio >= 7) bonus = "20%";
            }
            document.getElementById('out-bonus').innerText = bonus;
            document.getElementById('out-ecart').innerText = `Écart: ${ecart.toFixed(2)} €`;

            // Calcul salaires
            const charges = status === 'cadre' ? 0.25 : 0.22;
            const net = brut * (1 - charges);
            const ij = Math.min((brut / 30.42) * 0.5, 52.04);
            document.getElementById('out-net').innerText = `${net.toFixed(2)} €`;
            document.getElementById('out-ij').innerText = `${ij.toFixed(2)} €`;

            if(chartCaObj) {
                chartCaObj.data.datasets[0].data[2] = ca;
                chartCaObj.update();
            }
            if(chartSalaryObj) {
                chartSalaryObj.data.datasets[0].data = [net, brut - net];
                chartSalaryObj.update();
            }
        }

        function toast(msg) {
            const div = document.createElement('div');
            div.className = "fixed bottom-5 right-5 bg-[#5551FF] text-white py-3 px-6 rounded-2xl shadow-lg z-50 text-sm font-bold animate-bounce";
            div.innerText = msg;
            document.body.appendChild(div);
            setTimeout(() => div.remove(), 2500);
        }

        // --- SCRIPT ACCESSIBILITÉ VOCALE AU SURVOL TRANSMIS PAR L'UTILISATEUR ---
        (function() {
            let lastText = "";
            let hoverTimer = null;
            document.addEventListener('mouseover', (e) => {
                if(!sessionState.audio_on_hover) return;
                const el = e.target;
                if(!el) return;

                let targetEl = el;
                let textToRead = "";
                let depth = 0;

                while (targetEl && depth < 3) {
                    textToRead = targetEl.getAttribute('data-tts') || targetEl.innerText || targetEl.textContent;
                    if (targetEl.matches('h1, h2, h3, h4, p, span, li, button, .stMarkdown, .buse-card, label, .carousel-badge, [data-testid=stMarkdownContainer]')) {
                        break;
                    }
                    targetEl = targetEl.parentElement;
                    depth++;
                }

                if (textToRead && textToRead.trim().length > 0 && textToRead.trim().length < 300 && textToRead !== lastText) {
                    clearTimeout(hoverTimer);
                    hoverTimer = setTimeout(() => {
                        speakText(textToRead.trim());
                        lastText = textToRead;
                    }, 120);
                }
            });

            document.addEventListener('mouseout', () => {
                lastText = "";
            });
        })();

        // --- CHARGEMENT DE LA BASE DE DONNÉES DEPUIS GITHUB ---
        async function fetchExternalExperts() {
            try {
                const response = await fetch('./experts_data.json');
                if (response.ok) {
                    const data = await response.json();
                    if (data && data.sentinelles) {
                        EXPERT_DIRECTORY = data.sentinelles;
                        renderSentinelles();
                        console.log("Base de données d'experts chargée depuis experts_data.json.");
                    }
                }
            } catch (e) {
                console.warn("Impossible de charger experts_data.json. Utilisation de la base d'urgence.");
            }
        }

        document.addEventListener("DOMContentLoaded", () => {
            document.getElementById('copyright-year').innerText = new Date().getFullYear();
            fetchExternalExperts();
            initPrimesAndSalariesCharts();
            renderCarousel();
        });
    </script>
</body>
</html>
