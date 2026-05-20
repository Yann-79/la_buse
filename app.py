<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>La Buse - Assistant droits du travail</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.1/dist/chart.umd.min.js"></script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
        
        body {
            font-family: 'Inter', sans-serif;
        }
        
        .owl-logo {
            filter: drop-shadow(0 10px 15px rgba(85, 81, 255, 0.3));
        }
        
        .card-hover {
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }
        .card-hover:hover {
            transform: translateY(-8px);
            box-shadow: 0 20px 25px -5px rgb(0 0 0 / 0.1), 0 8px 10px -6px rgb(0 0 0 / 0.1);
        }
        
        .nav-active {
            background-color: #4f46e5 !important;
            color: white !important;
            border-radius: 9999px;
        }
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
            <p class="text-gray-500 mb-8">Entrez votre code PIN pour continuer</p>
            
            <input type="password" id="pin-input" maxlength="4" 
                   class="w-full text-center text-5xl tracking-[0.5em] py-6 bg-gray-100 rounded-2xl focus:outline-none focus:ring-4 focus:ring-indigo-300"
                   placeholder="••••">
            
            <button onclick="unlockApp()" 
                    class="mt-8 w-full bg-indigo-600 hover:bg-indigo-700 text-white font-semibold py-4 rounded-2xl text-lg transition-all active:scale-95">
                Déverrouiller
            </button>
            <p id="pin-error" class="text-red-500 mt-4 hidden">Code PIN incorrect</p>
        </div>
    </div>

    <div class="flex h-screen hidden" id="app">

        <!-- SIDEBAR -->
        <div class="w-72 bg-white border-r border-gray-200 flex flex-col">
            <div class="p-6 border-b flex items-center gap-3">
                <div class="w-11 h-11 bg-gradient-to-br from-indigo-600 to-purple-600 rounded-2xl flex items-center justify-center text-white text-3xl shadow-lg">
                    🦉
                </div>
                <div>
                    <h1 class="text-3xl font-bold tracking-tight text-gray-900">la buse</h1>
                    <p class="text-emerald-600 text-sm font-medium">Abonnement Actif</p>
                </div>
            </div>

            <nav class="flex-1 p-4 space-y-1">
                <button onclick="switchView('Accueil')" class="nav-btn w-full text-left px-5 py-3.5 flex items-center gap-3 text-gray-700 hover:bg-gray-100 rounded-2xl" data-view="Accueil">
                    🏠 Accueil
                </button>
                <button onclick="switchView('Eagle')" class="nav-btn w-full text-left px-5 py-3.5 flex items-center gap-3 text-gray-700 hover:bg-gray-100 rounded-2xl" data-view="Eagle">
                    🦅 Eagle Agent
                </button>
                <button onclick="switchView('Sentinelles')" class="nav-btn w-full text-left px-5 py-3.5 flex items-center gap-3 text-gray-700 hover:bg-gray-100 rounded-2xl" data-view="Sentinelles">
                    🛡️ Sentinelles
                </button>
                <button onclick="switchView('Primes')" class="nav-btn w-full text-left px-5 py-3.5 flex items-center gap-3 text-gray-700 hover:bg-gray-100 rounded-2xl" data-view="Primes">
                    💎 Calculateur Primes
                </button>
            </nav>
        </div>

        <!-- MAIN -->
        <div class="flex-1 flex flex-col">
            <header class="h-16 bg-white border-b px-8 flex items-center justify-between">
                <div class="relative w-96">
                    <input id="global-search" type="text" 
                           class="w-full bg-gray-100 rounded-full py-3 pl-12 focus:outline-none focus:ring-2 focus:ring-indigo-200"
                           placeholder="Rechercher une question ou un sujet...">
                    <span class="absolute left-5 top-3.5 text-gray-400">🔍</span>
                </div>
                <div class="flex items-center gap-4">
                    <div class="px-4 py-2 bg-emerald-50 text-emerald-700 rounded-2xl text-sm font-medium">Niort • 79</div>
                    <div class="flex items-center gap-3">
                        <div class="w-9 h-9 bg-indigo-100 rounded-2xl flex items-center justify-center font-bold text-indigo-700">A</div>
                        <div class="text-sm">
                            <p class="font-semibold">Alexandre</p>
                        </div>
                    </div>
                </div>
            </header>

            <div class="flex-1 overflow-auto p-8" id="main-content">
                <!-- Vue Accueil -->
                <div id="view-Accueil" class="view">
                    <h1 class="text-5xl font-bold leading-tight mb-6">
                        La buse, votre moteur de recherche<br>
                        <span class="text-indigo-600">au service du monde du travail.</span>
                    </h1>
                    <p class="text-xl text-gray-600 mb-10">Posez vos questions. Analysez vos documents. Défendez vos droits.</p>

                    <!-- Eagle Agent -->
                    <div class="bg-white rounded-3xl p-8 shadow">
                        <div class="flex gap-4 mb-6">
                            <span class="text-5xl">🦅</span>
                            <div>
                                <h2 class="text-2xl font-bold">Eagle Agent IA</h2>
                                <p class="text-gray-500">Analyse juridique instantanée</p>
                            </div>
                        </div>
                        <div class="flex gap-3">
                            <input id="home-query" type="text" class="flex-1 bg-gray-100 rounded-2xl px-6 py-5 focus:outline-none focus:ring-2 focus:ring-indigo-300" 
                                   placeholder="Ex: Quelles sont mes indemnités de licenciement ?">
                            <button onclick="triggerAnalysis()" 
                                    class="bg-indigo-600 hover:bg-indigo-700 text-white px-10 rounded-2xl font-semibold">
                                Analyser
                            </button>
                        </div>
                        <div id="analysis-result" class="hidden mt-8 p-6 bg-indigo-50 rounded-2xl"></div>
                    </div>
                </div>
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
            const el = document.getElementById(`view-${view}`);
            if (el) el.classList.remove('hidden');

            document.querySelectorAll('.nav-btn').forEach(btn => {
                btn.classList.toggle('nav-active', btn.dataset.view === view);
            });
        }

        function triggerAnalysis() {
            const query = document.getElementById('home-query').value.trim();
            if (!query) return;

            const resultDiv = document.getElementById('analysis-result');
            resultDiv.classList.remove('hidden');
            resultDiv.innerHTML = `
                <h3 class="font-bold text-indigo-700 mb-3">Analyse Eagle Agent</h3>
                <p class="font-medium">Question : ${query}</p>
                <div class="mt-6 text-gray-700 leading-relaxed">
                    Selon le Code du travail et la jurisprudence, voici l'analyse...
                </div>
                <button onclick="this.parentElement.classList.add('hidden')" class="mt-6 text-indigo-600 hover:underline text-sm">
                    Fermer
                </button>
            `;
        }

        // Touche Entrée sur le PIN
        document.getElementById('pin-input').addEventListener('keypress', (e) => {
            if (e.key === 'Enter') unlockApp();
        });
    </script>
</body>
</html>
