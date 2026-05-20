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
            background-color: #4f46e5;
            color: white;
            border-radius: 9999px;
        }
    </style>
</head>
<body class="bg-gray-50 text-gray-900 min-h-screen">

    <!-- PIN SCREEN -->
    <div id="pin-screen" class="fixed inset-0 bg-white z-50 flex items-center justify-center">
        <div class="max-w-sm w-full px-6 text-center">
            <div class="mx-auto w-32 h-32 bg-gradient-to-br from-indigo-500 to-purple-600 rounded-3xl flex items-center justify-center owl-logo mb-8">
                <span class="text-6xl">🦉</span>
            </div>
            <h2 class="text-3xl font-bold mb-2">Accès sécurisé</h2>
            <p class="text-gray-500 mb-8">Entrez votre code PIN</p>
            
            <input type="password" id="pin-input" maxlength="4" 
                   class="w-full text-center text-4xl tracking-widest py-6 bg-gray-100 rounded-2xl focus:outline-none focus:ring-4 focus:ring-indigo-300"
                   placeholder="••••">
            
            <button onclick="unlockApp()" 
                    class="mt-6 w-full bg-indigo-600 hover:bg-indigo-700 text-white font-semibold py-4 rounded-2xl transition">
                Déverrouiller
            </button>
            <p id="pin-error" class="text-red-500 mt-4 hidden">Code PIN incorrect</p>
        </div>
    </div>

    <div class="flex h-screen" id="app" style="display: none
