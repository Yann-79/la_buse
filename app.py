<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>La Buse - Assistant intelligent droits du travail</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    
    <style>
        body { font-family: 'Inter', sans-serif; }
        .owl-logo { filter: drop-shadow(0 10px 15px rgba(85, 81, 255, 0.3)); }
        .card-hover:hover { transform: translateY(-8px); box-shadow: 0 20px 25px -5px rgb(0 0 0 / 0.1); }
        .nav-active { background-color: #4f46e5; color: white; border-radius: 9999px; }
    </style>
</head>
<body class="bg-gray-50 text-gray-900">

    <!-- PIN SCREEN -->
    <div id="pin-screen" class="fixed inset-0 bg-white z-50 flex items-center justify-center">
        <div class="max-w-sm w-full px-6 text-center">
            <div class="mx-auto w-32 h-32 bg-gradient-to-br from-indigo-600 to-purple-600 rounded-3xl flex items-center justify-center text-7xl mb-8 owl-logo">
                🦉
            </div>
            <h2 class="text-3xl font-bold mb-2">Accès sécurisé</h2>
            <p class="text-gray-500 mb-8">Saisissez votre code PIN</p>
            <input type="password" id="pin-input" maxlength="4" class="w-full text-center text-5xl tracking-widest py-6 bg-gray-100 rounded-2xl focus:outline-none focus:ring-4 focus:ring-indigo-300" placeholder="••••">
            <button onclick="unlockApp()" class="mt-8 w-full bg-indigo-600 hover:bg-indigo-700 text-white font-semibold py-4 rounded-2xl text-lg">Déverrouiller</button>
            <p id="pin-error" class="hidden text-red-500 mt-4">Code PIN incorrect</p>
        </div>
    </div>

    <div class="flex h-screen hidden" id="app">

        <!-- SIDEBAR MODERNE (inspiré Photo 2) -->
        <div class="w-72 bg-white border-r shadow-xl flex flex-col">
            <div class="p-6 border-b flex items-center gap-3">
                <div class="w-11 h-11 bg-gradient-to-br from-indigo-600 to-purple-600 rounded-2xl flex items-center justify-center text-white text-3xl owl-logo">
                    🦉
                </div>
                <div>
                    <h1 class="text-3xl font-bold tracking-tight">la buse</h1>
                    <p class="text-emerald-600 text-sm font-medium">Abonnement Actif</p>
                </div>
            </div>

            <nav class="flex-1 p-4 space-y-1">
                <button onclick="switchView('Accueil')" class="nav-btn w-full text-left px-5 py-3.5 flex items-center gap-3 hover:bg-gray-100 rounded-2xl" data-view="Accueil">🏠 Accueil</button>
                <button onclick="switchView('Eagle')" class="nav-btn w-full text-left px-5 py-3.5 flex items-center gap-3 hover:bg-gray-100 rounded-2xl" data-view="Eagle">🦅 Eagle Agent</button>
                <button onclick="switchView('Sentinelles')" class="nav-btn w-full text-left px-5 py-3.5 flex items-center gap-3 hover:bg-gray-100 rounded-2xl" data-view="Sentinelles">🛡️ Sentinelles</button>
                <button onclick="switchView('Primes')" class="nav-btn w-full text-left px-5 py-3.5 flex items-center gap-3 hover:bg-gray-100 rounded-2xl" data-view="Primes">💎 Primes & Salaires</button>
                <button onclick="switchView('Conges')" class="nav-btn w-full text-left px-5 py-3.5 flex items-center gap-3 hover:bg-gray-100 rounded-2xl" data-view="Conges">🏖️ Congés & RTT</button>
            </nav>
        </div>

        <!-- MAIN CONTENT -->
        <div class="flex-1 flex flex-col overflow-hidden">

            <!-- HEADER -->
            <header class="h-16 bg-white border-b px-8 flex items-center justify-between">
                <div class="relative w-96">
                    <input id="global-search" type="text" class="w-full bg-gray-100 rounded-full py-3 pl-12 focus:outline-none focus:ring-2 focus:ring-indigo-300" placeholder="Rechercher une question, un document...">
                    <span class="absolute left-5 top-3.5 text-gray-400">🔍</span>
                </div>
                <div class="flex items-center gap-4">
                    <div class="px-4 py-2 bg-emerald-50 text-emerald-700 rounded-2xl text-sm font-medium">Niort • 79</div>
                    <div class="flex items-center gap-3">
                        <div class="w-9 h-9 bg-indigo-100 rounded-2xl flex items-center justify-center font-bold text-indigo-700">A</div>
                        <span class="font-medium">Alexandre</span>
                    </div>
                </div>
            </header>

            <!-- CONTENT -->
            <div class="flex-1 p-8 overflow-auto" id="main-content">

                <!-- ACCUEIL -->
                <div id="view-Accueil" class="view">
                    <div class="max-w-6xl mx-auto">
                        <div class="flex justify-between items-start mb-10">
                            <div>
                                <h1 class="text-5xl font-bold leading-tight">La buse, votre moteur<br>de recherche au service<br><span class="text-indigo-600">du monde du travail.</span></h1>
                                <p class="text-xl text-gray-600 mt-4">Posez vos questions • Analysez vos documents • Défendez vos droits</p>
                            </div>
                            <div class="text-8xl">🦉</div>
                        </div>

                        <!-- Eagle Agent -->
                        <div class="bg-white rounded-3xl p-8 shadow-sm">
                            <div class="flex items-center gap-4 mb-6">
                                <span class="text-5xl">🦅</span>
                                <div>
                                    <h2 class="text-2xl font-bold">Eagle Agent IA</h2>
                                    <p class="text-gray-500">Audit intelligent de contrats, fiches de paie et contestations</p>
                                </div>
                            </div>
                            <div class="flex gap-3">
                                <input id="home-query" type="text" class="flex-1 bg-gray-100 rounded-2xl px-6 py-5 focus:outline-none focus:ring-2 focus:ring-indigo-300" placeholder="Ex: Mon contrat est-il conforme ? Analyse ma fiche de paie...">
                                <button onclick="triggerAnalysis()" class="bg-indigo-600 hover:bg-indigo-700 text-white px-10 rounded-2xl font-semibold">Analyser</button>
                            </div>
                            <div id="analysis-result" class="hidden mt-8 p-6 bg-indigo-50 rounded-2xl"></div>
                        </div>
                    </div>
                </div>

                <!-- Autres vues à développer -->
                <div id="view-Eagle" class="view hidden">Eagle Agent - Chatbot avancé</div>
                <div id="view-Sentinelles" class="view hidden">Réseau Sentinelles</div>
                <div id="view-Primes" class="view hidden">Calculateur Primes</div>
                <div id="view-Conges" class="view hidden">Congés & RTT</div>

            </div>
        </div>
    </div>

    <script>
        function unlockApp() {
            if (document.getElementById('pin-input').value === '1234') {
                document.getElementById('pin-screen').classList.add('hidden');
                document.getElementById('app').classList.remove('hidden');
                switchView('Accueil');
            } else {
                document.getElementById('pin-error').classList.remove('hidden');
            }
        }

        function switchView(view) {
            document.querySelectorAll('.view').forEach(v => v.classList.add('hidden'));
            const active = document.getElementById(`view-${view}`);
            if (active) active.classList.remove('hidden');
        }

        function triggerAnalysis() {
            const query = document.getElementById('home-query').value.trim();
            if (!query) return;
            
            const result = document.getElementById('analysis-result');
            result.classList.remove('hidden');
            result.innerHTML = `
                <h3 class="font-bold text-indigo-700 mb-3">Analyse Eagle Agent</h3>
                <p class="font-medium">Question : ${query}</p>
                <div class="mt-6 text-gray-700 leading-relaxed">
                    Selon les informations de votre contrat et les textes en vigueur, voici l'analyse détaillée...
                </div>
            `;
        }

        // Touche Entrée sur PIN
        document.getElementById('pin-input').addEventListener('keypress', (e) => {
            if (e.key === 'Enter') unlockApp();
        });
    </script>
</body>
</html>
