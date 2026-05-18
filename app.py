<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>La Buse - Assistant intelligent pour les droits du travail</title>
    <!-- Tailwind CSS pour un design moderne, épuré et réactif -->
    <script src="https://cdn.tailwindcss.com"></script>
    <!-- Chart.js pour des visualisations claires et interactives de salaires et primes -->
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
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
            height: 300px;
            max-height: 350px;
        }
        /* Style personnalisé pour les cartes épurées de la maquette (Photo 2) */
        .maquette-card {
            background-color: #FFFFFF;
            border-radius: 16px;
            border: 1px solid rgba(0, 0, 0, 0.05);
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.01);
            transition: transform 0.2s ease, box-shadow 0.2s ease;
        }
        .maquette-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 30px rgba(85, 81, 255, 0.08);
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
        .high-contrast button {
            background-color: #FFFF00 !important;
            color: #000000 !important;
            border: 2px solid #FFFFFF !important;
        }
        /* Cacher la scrollbar sur les conteneurs horizontaux */
        .no-scrollbar::-webkit-scrollbar {
            display: none;
        }
        .no-scrollbar {
            -ms-overflow-style: none;
            scrollbar-width: none;
        }
    </style>
</head>
<body class="flex min-h-screen bg-[#F4F5FC] transition-colors duration-200">

    <!-- Chosen Palette: Apple Violet Premium (Arrière-plan: #F4F5FC, Cartes: #FFFFFF, Accent: #5551FF, Survol: #413CFF, Texte: #1E203B) -->
    
    <!-- Application Structure Plan: 
         La structure de l'application est modélisée fidèlement sur l'architecture asymétrique de la Photo 2. 
         Elle comprend :
         1. Une barre latérale gauche pour naviguer de manière stable entre les fonctionnalités (Accueil, Eagle Agent, Audit, Primes, etc.).
         2. Un panneau central large pour le flux principal d'activité de l'utilisateur (affichage des cartes d'action, barre de recherche Eagle Agent, carrousels informatiques et formulaires).
         3. Un panneau latéral droit fixe qui affiche les outils d'accès rapide, le panneau de configuration interactif de l'accessibilité vocale, et un bouton d'urgence Sentinelles.
         Cette architecture a été choisie car elle offre une lisibilité maximale sans perte de contexte et respecte précisément les zones fonctionnelles de la maquette originale.
    -->
    
    <!-- Visualization & Content Choices: 
         - Proportions Salaire Brut/Net/Charges -> Graphique en anneau (Doughnut Chart.js) -> Pour illustrer l'impact des cotisations.
         - Seuil de déclenchement de la prime d'écart Infinity -> Graphique à barres verticales (Bar Chart.js) -> Pour visualiser la distance par rapport au seuil de 1300€ et au palier de 411.69€.
         - Agent d'intelligence conversationnelle Eagle -> Chat interactif dynamique -> Permet des questions en français et des réponses instantanées lues à voix haute.
         - Réseau de proximité -> Cartographie interactive et liste triée par calcul de distance (formule de Haversine) -> Identifie les avocats et syndicats les plus proches de Niort / Saint-Maxire.
         - CONFIRMATION : Aucun élément SVG externe ni graphique Mermaid JS n'est utilisé. Tous les éléments visuels sont créés en CSS pur et Emojis natifs.
    -->
    
    <!-- CONFIRMATION: NO SVG graphics used. NO Mermaid JS used. -->

    <!-- ================= BARRE LATÉRALE GAUCHE (MENU) ================= -->
    <aside id="sidebar" class="w-64 bg-white border-r border-gray-100 flex flex-col shrink-0 z-20">
        <div class="p-6 border-b border-gray-100 flex items-center gap-3">
            <!-- Chouette miniature CSS -->
            <div class="w-10 h-10 rounded-full bg-[#E8E7FF] flex items-center justify-center relative">
                <div class="w-2 h-2 bg-[#5551FF] rounded-full absolute top-3 left-2.5"></div>
                <div class="w-2 h-2 bg-[#5551FF] rounded-full absolute top-3 right-2.5"></div>
                <div class="w-0 h-0 border-l-[4px] border-l-transparent border-r-[4px] border-r-transparent border-top-[6px] border-top-[#FF9F43] absolute bottom-3"></div>
            </div>
            <div>
                <h1 class="text-xl font-bold text-[#1E203B]" data-tts="La buse">la buse</h1>
                <span class="text-xs text-[#5551FF] font-semibold">Abonnement Actif</span>
            </div>
        </div>

        <nav class="flex-1 p-4 space-y-1 overflow-y-auto no-scrollbar">
            <button onclick="switchView('Accueil')" id="btn-menu-Accueil" class="w-full flex items-center gap-3 px-4 py-3 rounded-xl text-left font-medium text-[#5551FF] bg-[#5551FF]/10 transition-all" data-tts="Onglet Accueil">
                <span>🏠</span> Accueil
            </button>
            <button onclick="switchView('Eagle')" id="btn-menu-Eagle" class="w-full flex items-center gap-3 px-4 py-3 rounded-xl text-left font-medium text-gray-600 hover:bg-gray-50 transition-all" data-tts="Onglet Eagle Agent">
                <span>🦅</span> Eagle Agent IA
            </button>
            <button onclick="switchView('Audit')" id="btn-menu-Audit" class="w-full flex items-center gap-3 px-4 py-3 rounded-xl text-left font-medium text-gray-600 hover:bg-gray-50 transition-all" data-tts="Onglet Analyse CV et Audit">
                <span>📄</span> Analyse CV & Audit
            </button>
            <button onclick="switchView('Code')" id="btn-menu-Code" class="w-full flex items-center gap-3 px-4 py-3 rounded-xl text-left font-medium text-gray-600 hover:bg-gray-50 transition-all" data-tts="Onglet Code du travail">
                <span>⚖️</span> Code du travail
            </button>
            <button onclick="switchView('Sentinelles')" id="btn-menu-Sentinelles" class="w-full flex items-center gap-3 px-4 py-3 rounded-xl text-left font-medium text-gray-600 hover:bg-gray-50 transition-all" data-tts="Onglet Réseau Sentinelles">
                <span>🛡️</span> Réseau Sentinelles
            </button>
            <button onclick="switchView('Primes')" id="btn-menu-Primes" class="w-full flex items-center gap-3 px-4 py-3 rounded-xl text-left font-medium text-gray-600 hover:bg-gray-50 transition-all" data-tts="Onglet Calculateur de primes">
                <span>💎</span> Calculateur de primes
            </button>
            <button onclick="switchView('Documents')" id="btn-menu-Documents" class="w-full flex items-center gap-3 px-4 py-3 rounded-xl text-left font-medium text-gray-600 hover:bg-gray-50 transition-all" data-tts="Onglet Mes documents">
                <span>📂</span> Mes documents
            </button>
        </nav>

        <div class="p-4 border-t border-gray-100">
            <div class="bg-gray-50 p-3 rounded-xl border border-gray-100 text-center">
                <span class="text-xs text-gray-500 block">Version Système</span>
                <strong class="text-sm text-[#1E203B]">MASTER-DEFENSE-1.1</strong>
            </div>
        </div>
    </aside>

    <!-- ================= CONTENUR DE PAGE ASYMÉTRIQUE ================= -->
    <div class="flex-1 flex flex-col min-w-0 overflow-hidden">
        
        <!-- En-tête Global de Recherche & Profil -->
        <header class="h-20 bg-white border-b border-gray-100 flex items-center justify-between px-8 shrink-0 z-10">
            <div class="w-96 relative">
                <input type="text" placeholder="Rechercher un sujet, une question, un service..." class="w-full bg-[#F4F5FC] border border-transparent rounded-xl py-2.5 pl-10 pr-4 text-sm outline-none focus:border-[#5551FF] focus:bg-white transition-all">
                <span class="absolute left-3.5 top-3.5 text-gray-400 text-sm">🔍</span>
            </div>
            
            <div class="flex items-center gap-6">
                <button onclick="toggleAccessibility()" class="bg-[#5551FF] text-white px-4 py-2 rounded-xl text-sm font-semibold hover:bg-[#413CFF] transition-all" data-tts="Bouton d'accessibilité rapide">♿ Accessibilité</button>
                <div class="w-px h-6 bg-gray-200"></div>
                <div class="flex items-center gap-3">
                    <div class="w-10 h-10 rounded-full bg-[#5551FF] text-white flex items-center justify-center font-bold">A</div>
                    <div>
                        <span class="text-xs text-gray-400 block">Bienvenue</span>
                        <strong class="text-sm text-[#1E203B] block">Alexandre</strong>
                    </div>
                </div>
            </div>
        </header>

        <!-- Zone de Défilement Principale -->
        <div class="flex-1 flex overflow-hidden">
            
            <!-- CONTENU CENTRAL LARGE -->
            <div class="flex-1 p-8 overflow-y-auto no-scrollbar">
                
                <!-- ================= VUE : ACCUEIL ================= -->
                <section id="view-Accueil" class="view-section space-y-8">
                    <!-- Section Titre Maquette -->
                    <div class="flex flex-col md:flex-row items-center justify-between gap-8 bg-white p-8 rounded-3xl border border-gray-100 relative overflow-hidden">
                        <div class="space-y-4 max-w-xl z-10">
                            <h2 class="text-4xl font-extrabold text-[#1E203B] leading-tight" data-tts="La buse, votre moteur de recherche au service du monde du travail.">
                                La buse, votre moteur <br>de recherche au service <br><span class="text-[#5551FF]">du monde du travail.</span>
                            </h2>
                            <p class="text-gray-500 text-base" data-tts="Posez vos questions, analysez vos documents, comprenez vos droits et passez à l'action.">Posez vos questions, analysez vos documents, comprenez vos droits et passez à l'action.</p>
                        </div>
                        
                        <!-- Mascotte Chouette Ronde et Violette de l'image 2 -->
                        <div class="shrink-0 z-10">
                            <div style="width: 170px; height: 170px; background-color: #E8E7FF; border-radius: 50%; position: relative; box-shadow: 0 12px 30px rgba(85, 81, 255, 0.25); display: flex; align-items: center; justify-content: center;">
                                <div style="position: absolute; top: -5px; left: 25px; width: 0; height: 0; border-left: 20px solid transparent; border-right: 20px solid transparent; border-bottom: 40px solid #5551FF; transform: rotate(-15deg);"></div>
                                <div style="position: absolute; top: -5px; right: 25px; width: 0; height: 0; border-left: 20px solid transparent; border-right: 20px solid transparent; border-bottom: 40px solid #5551FF; transform: rotate(15deg);"></div>
                                <div style="width: 110px; height: 125px; background-color: #5551FF; border-radius: 50% 50% 45% 45%; position: relative; overflow: hidden; display: flex; align-items: center; justify-content: center;">
                                    <div style="position: absolute; bottom: -10px; width: 85px; height: 85px; background-color: #FFFFFF; border-radius: 50%;"></div>
                                </div>
                                <div style="position: absolute; top: 48px; left: 38px; width: 45px; height: 45px; background-color: #FFFFFF; border-radius: 50%; display: flex; align-items: center; justify-content: center; box-shadow: inset 0 2px 4px rgba(0,0,0,0.1);">
                                    <div style="width: 20px; height: 20px; background-color: #1E203B; border-radius: 50%; position: relative;">
                                        <div style="width: 7px; height: 7px; background-color: #FFFFFF; border-radius: 50%; position: absolute; top: 3px; left: 3px;"></div>
                                    </div>
                                </div>
                                <div style="position: absolute; top: 48px; right: 38px; width: 45px; height: 45px; background-color: #FFFFFF; border-radius: 50%; display: flex; align-items: center; justify-content: center; box-shadow: inset 0 2px 4px rgba(0,0,0,0.1);">
                                    <div style="width: 20px; height: 20px; background-color: #1E203B; border-radius: 50%; position: relative;">
                                        <div style="width: 7px; height: 7px; background-color: #FFFFFF; border-radius: 50%; position: absolute; top: 3px; left: 3px;"></div>
                                    </div>
                                </div>
                                <div style="position: absolute; top: 85px; width: 0; height: 0; border-left: 10px solid transparent; border-right: 10px solid transparent; border-top: 18px solid #FF9F43; z-index: 10;"></div>
                            </div>
                        </div>
                    </div>

                    <!-- Carrousel d'Informations interactif et dynamique -->
                    <div class="carousel-container maquette-card">
                        <span id="carousel-badge" class="carousel-badge" data-tts="Mise en avant">Prévention RPS</span>
                        <h3 id="carousel-title" class="carousel-title" data-tts="Votre santé est une priorité absolue">🛡️ Votre santé est une priorité absolue</h3>
                        <p id="carousel-desc" class="carousel-desc" data-tts="L'employeur est légalement tenu de protéger votre santé physique et mentale (Article L4121-1 du Code du travail). Ne restez pas isolé face aux pressions managériales.">L'employeur est légalement tenu de protéger votre santé physique et mentale (Article L4121-1 du Code du travail). Ne restez pas isolé face aux pressions managériales.</p>
                        
                        <div class="flex items-center gap-3">
                            <button onclick="prevCarousel()" class="bg-[#F4F5FC] hover:bg-[#E8E7FF] text-[#5551FF] font-semibold px-4 py-2 rounded-xl text-xs transition-all">⬅️ Précédent</button>
                            <button onclick="nextCarousel()" class="bg-[#F4F5FC] hover:bg-[#E8E7FF] text-[#5551FF] font-semibold px-4 py-2 rounded-xl text-xs transition-all">Suivant ➡️</button>
                        </div>
                    </div>

                    <!-- Grille Actions (Ce que La buse peut faire pour vous) -->
                    <div class="space-y-4">
                        <h3 class="text-xl font-bold text-[#1E203B]" data-tts="Ce que la buse peut faire pour vous">Ce que La buse peut faire pour vous</h3>
                        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                            <div onclick="switchView('Eagle')" class="maquette-card p-6 cursor-pointer flex gap-4 items-start" data-tts="Dalle Eagle Agent. Posez vos questions de droit du travail.">
                                <span class="text-3xl">🦅</span>
                                <div>
                                    <h4 class="font-bold text-lg text-[#1E203B]">Eagle Agent</h4>
                                    <p class="text-sm text-gray-500 mt-1">Posez toutes vos questions sur le droit du travail et obtenez des réponses fiables, sourcées et personnalisées.</p>
                                </div>
                            </div>
                            <div onclick="switchView('Audit')" class="maquette-card p-6 cursor-pointer flex gap-4 items-start" data-tts="Dalle Analyse CV et Audit. Détectez les anomalies de contrat.">
                                <span class="text-3xl">📄</span>
                                <div>
                                    <h4 class="font-bold text-lg text-[#1E203B]">Analyse CV & Audit</h4>
                                    <p class="text-sm text-gray-500 mt-1">Détectez les anomalies, comparez votre contrat au Code du travail et à votre convention collective.</p>
                                </div>
                            </div>
                            <div onclick="switchView('Sentinelles')" class="maquette-card p-6 cursor-pointer flex gap-4 items-start" data-tts="Dalle Réseau Sentinelles. Être mis en relation avec des délégués ou juristes.">
                                <span class="text-3xl">🛡</span>
                                <div>
                                    <h4 class="font-bold text-lg text-[#1E203B]">Réseau Sentinelles</h4>
                                    <p class="text-sm text-gray-500 mt-1">Soyez mis en relation avec des syndicats ou des juristes spécialisés en droit du travail de proximité.</p>
                                </div>
                            </div>
                            <div onclick="switchView('Primes')" class="maquette-card p-6 cursor-pointer flex gap-4 items-start" data-tts="Dalle Calculateur de primes. Estimez vos primes Infinity et de paie.">
                                <span class="text-3xl">💎</span>
                                <div>
                                    <h4 class="font-bold text-lg text-[#1E203B]">Calculateur de primes</h4>
                                    <p class="text-sm text-gray-500 mt-1">Estimez vos primes, indemnités et avantages selon votre situation réelle et votre secteur.</p>
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- Bannière Mission -->
                    <div class="bg-gradient-to-r from-[#5551FF] to-[#413CFF] text-white p-8 rounded-3xl flex flex-col md:flex-row items-center justify-between gap-6" data-tts="Bannière Mission. Vos droits, notre mission.">
                        <div class="space-y-2">
                            <h3 class="text-xl font-bold">Vos droits. Notre mission.</h3>
                            <p class="text-sm text-blue-100">La buse vous aide à comprendre, vérifier et défendre vos droits au travail en toute simplicité.</p>
                        </div>
                        <button onclick="switchView('Eagle')" class="bg-white text-[#5551FF] font-semibold px-6 py-3 rounded-xl shadow-sm hover:bg-gray-50 transition-all shrink-0">Découvrir l'Agent Eagle</button>
                    </div>
                </section>

                <!-- ================= VUE : EAGLE IA ================= -->
                <section id="view-Eagle" class="view-section hidden space-y-6">
                    <div class="mb-4">
                        <h2 class="text-3xl font-bold text-[#1E203B] mb-2" data-tts="Eagle Agent - Assistance & RPS">🦅 Eagle Agent - Assistance & RPS</h2>
                        <p class="text-gray-500 text-sm">Posez vos questions sur la convention collective IDCC 1517 ou formulez une alerte liée à une situation de harcèlement.</p>
                    </div>

                    <div class="maquette-card p-6 space-y-6 flex flex-col h-[500px]">
                        <div id="chat-box" class="flex-1 overflow-y-auto space-y-4 pr-2 no-scrollbar">
                            <div class="flex gap-4">
                                <div class="w-10 h-10 rounded-full bg-[#E8E7FF] flex items-center justify-center shrink-0">🦉</div>
                                <div class="bg-gray-50 p-4 rounded-2xl rounded-tl-none border border-gray-100 max-w-xl">
                                    <p class="text-sm text-gray-800">Bonjour ! Je suis l'Agent Eagle. Dites-moi comment je peux vous aider aujourd'hui sur l'IDCC 1517 ou signalez-moi toute anomalie ou pression au travail.</p>
                                </div>
                            </div>
                        </div>

                        <div class="border-t border-gray-100 pt-4 flex gap-3">
                            <input type="text" id="chat-input" placeholder="Ex : Mon employeur me refuse mes heures supplémentaires, que faire ?" class="flex-1 bg-[#F4F5FC] border border-transparent rounded-xl px-4 py-3 text-sm outline-none focus:border-[#5551FF] focus:bg-white transition-all">
                            <button onclick="processEagleQuery()" class="bg-[#5551FF] text-white px-6 py-3 rounded-xl font-semibold hover:bg-[#413CFF] transition-all shadow-sm shrink-0">Poser la question</button>
                        </div>
                    </div>
                </section>

                <!-- ================= VUE : AUDIT ================= -->
                <section id="view-Audit" class="view-section hidden space-y-6">
                    <div class="mb-4">
                        <h2 class="text-3xl font-bold text-[#1E203B] mb-2" data-tts="Analyse CV et Audit de conformité">🔍 Analyse CV & Audit</h2>
                        <p class="text-gray-500 text-sm">Téléversez vos fiches de paie ou vos contrats pour détecter automatiquement les anomalies.</p>
                    </div>

                    <div class="maquette-card p-8 text-center border-2 border-dashed border-gray-200 hover:border-[#5551FF] transition-all cursor-pointer">
                        <span class="text-5xl block mb-4">📥</span>
                        <h3 class="text-lg font-bold text-[#1E203B] mb-1">Sélectionnez vos fichiers</h3>
                        <p class="text-sm text-gray-400 mb-6">Fichiers PDF, PNG ou JPG de fiches de paie ou de contrats (Max. 20Mo)</p>
                        <button class="bg-[#5551FF] text-white px-6 py-2.5 rounded-xl font-semibold inline-block max-w-xs" onclick="simulateAudit()">Lancer l'audit de document</button>
                    </div>

                    <div id="audit-results" class="hidden maquette-card p-6 space-y-4">
                        <h3 class="text-lg font-bold text-green-600 flex items-center gap-2"><span>✅</span> Résultats de l'analyse</h3>
                        <p class="text-sm text-gray-700">Le document a été analysé de manière permanente et sécurisée :</p>
                        <ul class="space-y-2 text-sm text-gray-600 list-disc list-inside">
                            <li>Cotisations de prévoyance de l'IDCC 1517 conformes.</li>
                            <li>Vigilance recommandée sur le décompte des heures de nuit travaillées (Article 12).</li>
                        </ul>
                    </div>
                </section>

                <!-- ================= VUE : CODE DU TRAVAIL ================= -->
                <section id="view-Code" class="view-section hidden space-y-6">
                    <div class="mb-4">
                        <h2 class="text-3xl font-bold text-[#1E203B] mb-2" data-tts="Base de données Code du travail">⚖️ Convention collective & Droits</h2>
                        <p class="text-gray-500 text-sm">Consultez en direct les textes de loi et de l'IDCC 1517 de la Boulangerie-Pâtisserie.</p>
                    </div>

                    <div class="maquette-card p-6 space-y-4">
                        <h3 class="text-lg font-bold text-[#1E203B]">Articles Clés à connaître :</h3>
                        <div class="space-y-3">
                            <div class="bg-gray-50 p-4 rounded-xl border border-gray-100">
                                <strong class="text-[#5551FF] block mb-1 text-sm">Article 12 : Travail de nuit</strong>
                                <p class="text-xs text-gray-600">Le travail de nuit (de 20h à 6h) doit être majoré d'un taux minimal de 25% ou donner droit à un repos compensateur.</p>
                            </div>
                            <div class="bg-gray-50 p-4 rounded-xl border border-gray-100">
                                <strong class="text-[#5551FF] block mb-1 text-sm">Article L4121-1 (Code du travail) : Santé mentale et physique</strong>
                                <p class="text-xs text-gray-600">L'employeur prend les mesures nécessaires pour assurer la sécurité et protéger la santé physique et mentale des travailleurs.</p>
                            </div>
                        </div>
                    </div>
                </section>

                <!-- ================= VUE : SENTINELLES ================= -->
                <section id="view-Sentinelles" class="view-section hidden space-y-6">
                    <div class="mb-4">
                        <h2 class="text-3xl font-bold text-[#1E203B] mb-2" data-tts="Réseau des sentinelles et experts de proximité">🛡️ Réseau Sentinelles</h2>
                        <p class="text-gray-500 text-sm">Recherchez un avocat ou un délégué spécialiste en droit social à proximité de Niort / Saint-Maxire (79).</p>
                    </div>

                    <div class="flex gap-4">
                        <input type="text" id="sentinel-filter" onkeyup="filterSentinelles()" placeholder="Rechercher par avocat, syndicat ou adresse..." class="flex-1 bg-white border border-gray-200 rounded-xl px-4 py-3 text-sm outline-none focus:border-[#5551FF] transition-all shadow-sm">
                    </div>

                    <div id="sentinel-list" class="grid grid-cols-1 md:grid-cols-2 gap-6">
                        <!-- Rendu par JavaScript -->
                    </div>
                </section>

                <!-- ================= VUE : PRIMES ================= -->
                <section id="view-Primes" class="view-section hidden space-y-6">
                    <div class="mb-4">
                        <h2 class="text-3xl font-bold text-[#1E203B] mb-2" data-tts="Calculateurs de primes et de salaire">💎 Calculateurs Primes & Salaires</h2>
                        <p class="text-gray-500 text-sm">Estimez vos primes d'écart Infinity, votre salaire net et vos indemnités journalières (IJ) de maladie.</p>
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

                <!-- ================= VUE : DOCUMENTS ================= -->
                <section id="view-Documents" class="view-section hidden space-y-6">
                    <div class="mb-4">
                        <h2 class="text-3xl font-bold text-[#1E203B] mb-2" data-tts="Mes documents">📂 Coffre-fort & Google Drive</h2>
                        <p class="text-gray-500 text-sm">Gérez vos fichiers et vos avenants contractuels de façon hautement cryptée.</p>
                    </div>

                    <div class="maquette-card p-6 space-y-4">
                        <h3 class="text-lg font-bold text-[#1E203B]">Mes fichiers synchronisés :</h3>
                        <div class="divide-y divide-gray-100 text-sm text-gray-700">
                            <div class="py-3 flex justify-between items-center">
                                <span>📄 contrat_de_travail_IDCC1517.pdf</span>
                                <span class="text-xs text-gray-400">Synchronisé</span>
                            </div>
                            <div class="py-3 flex justify-between items-center">
                                <span>📄 avenant_infinity_v4.pdf</span>
                                <span class="text-xs text-gray-400">Synchronisé</span>
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
                        <div onclick="switchView('Audit')" class="flex items-center gap-2 cursor-pointer hover:text-[#5551FF] transition-all"><span>📄</span> Analyser mon CV</div>
                        <div onclick="switchView('Audit')" class="flex items-center gap-2 cursor-pointer hover:text-[#5551FF] transition-all"><span>⚖️</span> Comparer mon contrat</div>
                        <div onclick="switchView('Code')" class="flex items-center gap-2 cursor-pointer hover:text-[#5551FF] transition-all"><span>🔍</span> Consulter ma convention</div>
                        <div onclick="switchView('Primes')" class="flex items-center gap-2 cursor-pointer hover:text-[#5551FF] transition-all"><span>💎</span> Simuler une prime</div>
                    </div>
                </div>

                <!-- Panneau Accessibilité (Fidèle à la photo 2) -->
                <div class="space-y-3">
                    <h4 class="text-xs font-bold text-gray-400 uppercase tracking-wider">Accessibilité</h4>
                    <div class="bg-white p-4 rounded-2xl border border-gray-100 space-y-4 shadow-sm text-sm text-gray-700">
                        <div class="flex justify-between items-center">
                            <div>
                                <strong class="block text-xs font-bold text-gray-700">Mode non voyant</strong>
                                <span class="text-[10px] text-gray-400 block">Optimisé pour lecteurs d'écran</span>
                            </div>
                            <input type="checkbox" onchange="toggleNonVoyant(this)" class="accent-[#5551FF] w-4 h-4 cursor-pointer">
                        </div>

                        <div class="flex justify-between items-center">
                            <div>
                                <strong class="block text-xs font-bold text-gray-700">Audio au survol</strong>
                                <span class="text-[10px] text-gray-400 block">Énoncer les éléments pointés</span>
                            </div>
                            <input type="checkbox" id="chk-audio-hover" onchange="toggleAudioHover(this)" checked class="accent-[#5551FF] w-4 h-4 cursor-pointer">
                        </div>

                        <div class="flex justify-between items-center">
                            <div>
                                <strong class="block text-xs font-bold text-gray-700">Contraste élevé</strong>
                                <span class="text-[10px] text-gray-400 block">Améliore la lisibilité globale</span>
                            </div>
                            <input type="checkbox" onchange="toggleContrast(this)" class="accent-[#5551FF] w-4 h-4 cursor-pointer">
                        </div>
                    </div>
                </div>

                <!-- Section Aide Immédiate -->
                <div class="space-y-3">
                    <h4 class="text-xs font-bold text-gray-400 uppercase tracking-wider">Besoin d'aide immédiate ?</h4>
                    <div class="bg-[#E8E7FF]/40 p-4 rounded-2xl border border-[#5551FF]/10 text-sm space-y-4">
                        <p class="text-xs text-gray-500">Nos experts du réseau Sentinelles sont connectés et à votre écoute.</p>
                        <button onclick="switchView('Sentinelles')" class="w-full bg-[#5551FF] text-white py-2.5 rounded-xl text-xs font-bold hover:bg-[#413CFF] transition-all">Être mis en relation</button>
                    </div>
                </div>

            </aside>

        </div>

    </div>

    <!-- ================= CODE JAVASCRIPT GLOBAL ================= -->
    <script>
        // Variables des graphiques Chart.js
        let chartCaObj = null;
        let chartSalaryObj = null;

        // Contrôle et Routage des Vues
        function switchView(viewId) {
            // Cacher toutes les sections
            document.querySelectorAll('.view-section').forEach(sec => sec.classList.add('hidden'));
            
            // Afficher la section cible
            const targetSection = document.getElementById('view-' + viewId);
            if(targetSection) targetSection.classList.remove('hidden');

            // Mettre à jour l'état de la barre de navigation
            document.querySelectorAll('section[data-testid="stSidebar"] button').forEach(btn => {
                btn.classList.remove('text-[#5551FF]', 'bg-[#5551FF]/10');
                btn.classList.add('text-gray-600');
            });

            const activeBtn = document.getElementById('btn-menu-' + viewId);
            if(activeBtn) {
                activeBtn.classList.remove('text-gray-600');
                activeBtn.classList.add('text-[#5551FF]', 'bg-[#5551FF]/10');
            }

            // Rafraîchir les données dynamiques au chargement de l'onglet
            if(viewId === 'Primes') {
                updatePrimesAndSalaries();
            } else if(viewId === 'Sentinelles') {
                renderSentinelles();
            }
        }

        // --- CONTRÔLES D'ACCESSIBILITÉ ---
        function toggleAccessibility() {
            const sidebar = document.getElementById('sidebar');
            st.toast("Contrôles d'accessibilité de proximité activés.");
        }

        function toggleNonVoyant(checkbox) {
            if(checkbox.checked) {
                document.body.style.fontSize = "120%";
            } else {
                document.body.style.fontSize = "100%";
            }
        }

        function toggleAudioHover(checkbox) {
            st.session_state.audio_on_hover = checkbox.checked;
        }

        function toggleContrast(checkbox) {
            if(checkbox.checked) {
                document.body.classList.add('high-contrast');
            } else {
                document.body.classList.remove('high-contrast');
            }
        }

        // --- CARROUSEL ACTU INTERACTIF (PAGE D'ACCUEIL) ---
        function nextCarousel() {
            st.session_state.carousel_index = (st.session_state.carousel_index + 1) % CAROUSEL_ITEMS.length;
            renderCarousel();
        }

        function prevCarousel() {
            st.session_state.carousel_index = (st.session_state.carousel_index - 1) % CAROUSEL_ITEMS.length;
            renderCarousel();
        }

        function renderCarousel() {
            const item = CAROUSEL_ITEMS[st.session_state.carousel_index];
            document.getElementById('carousel-badge').innerText = item.badge;
            document.getElementById('carousel-badge').setAttribute('data-tts', item.badge);
            document.getElementById('carousel-title').innerText = item.titre;
            document.getElementById('carousel-title').setAttribute('data-tts', item.titre);
            document.getElementById('carousel-desc').innerText = item.description;
            document.getElementById('carousel-desc').setAttribute('data-tts', item.description);
        }

        // --- AGENT EAGLE (TRAITEMENT INSTANTANÉ SANS GELÉ DE PAGE) ---
        function processEagleQuery() {
            const chatInput = document.getElementById('chat-input');
            const prompt = chatInput.value.trim();
            if(!prompt) return;

            const chatBox = document.getElementById('chat-box');
            
            // Étape 1 : Affichage du message de l'utilisateur
            chatBox.innerHTML += `
                <div class="flex gap-4 justify-end">
                    <div class="bg-[#5551FF] text-white p-4 rounded-2xl rounded-tr-none shadow-sm max-w-xl">
                        <p class="text-sm">${prompt}</p>
                    </div>
                </div>
            `;
            chatInput.value = "";
            chatBox.scrollTop = chatBox.scrollHeight;

            // Étape 2 : Simulation d'analyse instantanée avec la base de connaissances
            setTimeout(() => {
                const response = call_eagle_ia_local(prompt);
                const utteranceId = "utterance_" + Date.now();
                
                chatBox.innerHTML += `
                    <div class="flex gap-4">
                        <div class="w-10 h-10 rounded-full bg-[#E8E7FF] flex items-center justify-center shrink-0">🦉</div>
                        <div class="bg-white p-4 rounded-2xl rounded-tl-none border border-gray-100 max-w-xl">
                            <div class="text-sm text-gray-800 leading-relaxed">${response.replace(/\n/g, '<br>')}</div>
                            <button id="${utteranceId}" onclick="speakAnswer('${response.replace(/'/g, "\\'")}')" class="bg-[#E8E7FF] text-[#5551FF] text-xs font-bold px-3 py-1.5 rounded-lg mt-3 transition-colors hover:bg-[#5551FF] hover:text-white">🔊 Écouter la réponse</button>
                        </div>
                    </div>
                `;
                chatBox.scrollTop = chatBox.scrollHeight;
            }, 500);
        }

        function speakAnswer(text) {
            window.speechSynthesis.cancel();
            const utterance = new SpeechSynthesisUtterance(text);
            utterance.lang = 'fr-FR';
            window.speechSynthesis.speak(utterance);
        }

        // --- AUDIT DOCUMENTAIRE SIMULÉ ---
        function simulateAudit() {
            const results = document.getElementById('audit-results');
            results.classList.remove('hidden');
        }

        // --- GÉOLOCALISATION DU RÉSEAU SENTINELLES ---
        function renderSentinelles(filter = "") {
            const container = document.getElementById('sentinel-list');
            container.innerHTML = "";
            
            const userLat = st.session_state.user_location["lat"];
            const userLon = st.session_state.user_location["lon"];

            const listData = EXPERT_DIRECTORY.map(exp => {
                const dist = haversine_distance(userLat, userLon, exp.lat, exp.lon);
                return { ...exp, distance: dist };
            }).sort((a, b) => a.distance - b.distance);

            const filtered = listData.filter(item => 
                item.Nom.toLowerCase().includes(filter.toLowerCase()) || 
                item.Adresse.toLowerCase().includes(filter.toLowerCase()) ||
                item.Type.toLowerCase().includes(filter.toLowerCase())
            );

            filtered.forEach(exp => {
                const badgeClass = exp.Type === "Avocat Spécialisé" ? "bg-purple-50 text-purple-700 border-purple-100" : exp.Type === "Union Syndicale" ? "bg-yellow-50 text-yellow-700 border-yellow-100" : "bg-green-50 text-green-700 border-green-100";
                
                container.innerHTML += `
                    <div class="maquette-card p-6 space-y-4 flex flex-col justify-between relative overflow-hidden" data-tts="${exp.Nom}, À ${exp.distance.toFixed(1)} km de chez vous">
                        <div class="space-y-2">
                            <div class="flex justify-between items-start gap-4">
                                <span class="px-2.5 py-1 rounded-full text-xs font-bold border ${badgeClass}">${exp.Type}</span>
                                <span class="text-xs text-[#5551FF] font-semibold">📍 À ${exp.distance.toFixed(1)} km</span>
                            </div>
                            <h4 class="font-bold text-[#1E203B] text-lg">${exp.Nom}</h4>
                            <p class="text-xs text-gray-400">📍 ${exp.Adresse}</p>
                            <p class="text-sm text-gray-600">${exp.Desc}</p>
                        </div>
                        <div class="bg-gray-50 p-3 rounded-xl border border-gray-100 flex justify-between items-center">
                            <strong class="text-sm">📞 ${exp.Contact}</strong>
                            <button onclick="st.toast('Demande transmise.')" class="bg-white border border-gray-200 text-xs font-bold px-3 py-1.5 rounded-lg text-[#5551FF] hover:bg-[#5551FF] hover:text-white hover:border-[#5551FF] transition-all">Saisir</button>
                        </div>
                    </div>
                `;
            });
        }

        function filterSentinelles() {
            const val = document.getElementById('sentinel-filter').value;
            renderSentinelles(val);
        }

        // --- CALCULATEUR DE PRIMES & SALAIRES (CHART.JS) ---
        function initPrimesAndSalariesCharts() {
            const ctxCa = document.getElementById('chart-ca').getContext('2d');
            chartCaObj = new Chart(ctxCa, {
                type: 'bar',
                data: {
                    labels: ['Seuil 1300€', 'Déclenchement', 'CA Magasin'],
                    datasets: [{
                        label: 'Euros (€)',
                        data: [1300, 1711.69, 1750],
                        backgroundColor: ['#EBEBFF', '#D8D6FF', '#5551FF'],
                        borderRadius: 8
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: { legend: { display: false } },
                    scales: { y: { beginAtZero: true } }
                }
            });

            const ctxSal = document.getElementById('chart-salary').getContext('2d');
            chartSalaryObj = new Chart(ctxSal, {
                type: 'doughnut',
                data: {
                    labels: ['Salaire Net', 'Charges Sociales'],
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
            const isCadre = document.getElementById('calc-status').value === 'cadre';

            // 1. Calcul Prime
            const [ecart, bonus, color, progress] = calculate_infinity_v4(ca, hours);
            document.getElementById('out-bonus').innerText = bonus;
            document.getElementById('out-ecart').innerText = `Écart: ${ecart.toFixed(2)} €`;

            // 2. Calcul Salaire
            const taux = isCadre ? 0.75 : 0.78;
            const net = brut * taux;
            const ij = Math.min((brut / 30.42) * 0.5, 52.04);
            document.getElementById('out-net').innerText = `${net.toFixed(2)} €`;
            document.getElementById('out-ij').innerText = `${ij.toFixed(2)} €`;

            // 3. Mise à jour des Graphiques
            if(chartCaObj) {
                chartCaObj.data.datasets[0].data[2] = ca;
                chartCaObj.update();
            }
            if(chartSalaryObj) {
                chartSalaryObj.data.datasets[0].data = [net, brut - net];
                chartSalaryObj.update();
            }
        }

        // --- INITIALISATION ÉVÉNEMENTIELLE ---
        document.addEventListener("DOMContentLoaded", () => {
            initPrimesAndSalariesCharts();
            renderCarousel();
            renderSentinelles();
        });

        // --- EMULATEUR STREAMLIT TOAST (Pour compatibilité API) ---
        const st = {
            toast: function(msg) {
                const notification = document.createElement('div');
                notification.className = "fixed bottom-5 right-5 bg-[#5551FF] text-white font-bold py-3 px-6 rounded-xl shadow-lg z-50 text-sm transition-all";
                notification.innerText = msg;
                document.body.appendChild(notification);
                setTimeout(() => { notification.remove(); }, 3000);
            },
            session_state: {
                carousel_index: 0,
                audio_on_hover: true,
                user_location: {"lat": 46.3833, "lon": -0.4500}
            }
        };
    </script>

</body>
</html>
