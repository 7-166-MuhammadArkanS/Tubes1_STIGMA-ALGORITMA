#Penjelasan singkat algoritma greedy
  Algoritma Greedy adalah pendekatan dalam pemrograman yang memecahkan persoalan optimasi dengan cara yang tampaknya rakus. Pendekatan ini berfokus pada pengambilan keputusan sekarang dengan harapan bahwa setiap langkah akan membawa kita lebih dekat ke solusi akhir yang optimal.

#Requirement program dan langkah-langkah
1. Menjalankan game engine
  -Node.js (https://nodejs.org/en)
  -Docker desktop (https://www.docker.com/products/docker-desktop/)
  -Yarn
    npm install --global yarn
    Gunakan cmd/command prompt bawaan device
  -Download source code (.zip) pada (https://github.com/haziqam/tubes1-IF2211-game-engine/releases/tag/v1.1.0)
  -Ekstrak file zip tersebut, lalu buka file lewat VSCode
  -Buka terminal di VSCode lalu ganti terminal Powershell(default) ke Command Prompt
  -Install dependencies menggunakan Yarn
    yarn
  -Setup default environment variable dengan menjalankan script berikut
    scripts/copy-env.bat (untuk windows)
    chmod +x ./scripts/copy-env.sh./scripts/copy-env.sh (untuk linux/macOS)
  -Buka docker dekstop, lalu buka terminal docker
  -Jalankan command berikut
    -docker compose up -d database
    -scripts/setup-db-prisma.bat (untuk windows)
     chmod +x ./scripts/setup-db-prisma.sh./scripts/setup-db-prisma.sh
  -Balik lagi ke terminal di VSCode, lalu lakukan Build
    npm run build
  -Setelah itu start game
    npm run start
  -Buka link di browser
    http://localhost:8082/

2. Menjalankan bot
   -Python (https://www.python.org/downloads/)
   -Download source code (.zip) pada (https://github.com/haziqam/tubes1-IF2211-bot-starter-pack/releases/tag/v1.0.1)
   -Ekstrak zip, lalu buka folder lewat VSCode
   -Buka terminal lewat VSCode lalu ganti terminal ke Command Prompt
   -Install dependencies menggunakan pip
     pip install -r requirements.txt
   -Setalah itu bot bisa dijalankan dengan command
     python main.py --logic Random --email=your_email@example.com --name=your_name --password=your_password --team etimo
  


  
