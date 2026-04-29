import os

files = [
    {
        "path": "backend/package.json",
        "content": '{\n  "name": "grouptaskhub-backend",\n  "version": "1.0.0",\n  "main": "src/index.ts",\n  "scripts": {\n    "start": "ts-node src/index.ts",\n    "dev": "nodemon src/index.ts",\n    "prisma:generate": "prisma generate",\n    "prisma:migrate": "prisma migrate dev"\n  },\n  "dependencies": {\n    "@prisma/client": "^5.x",\n    "bcrypt": "^5.1.1",\n    "cors": "^2.8.5",\n    "dotenv": "^16.4.5",\n    "express": "^4.19.2",\n    "jsonwebtoken": "^9.0.2"\n  },\n  "devDependencies": {\n    "@types/bcrypt": "^5.0.2",\n    "@types/cors": "^2.8.17",\n    "@types/express": "^4.17.21",\n    "@types/jsonwebtoken": "^9.0.6",\n    "@types/node": "^20.12.7",\n    "nodemon": "^3.1.0",\n    "prisma": "^5.x",\n    "ts-node": "^10.9.2",\n    "typescript": "^5.4.5"\n  }\n}'
    },
    {
        "path": "backend/prisma/schema.prisma",
        "content": 'datasource db {\n  provider = "postgresql"\n  url      = env("DATABASE_URL")\n}\n\ngenerator client {\n  provider = "prisma-client-js"\n}\n\nmodel User {\n  id            String   @id @default(uuid())\n  email         String   @unique\n  name          String\n  password_hash String\n  created_at    DateTime @default(now())\n  groups        GroupMember[]\n  owned_groups  Group[]\n}\n\nmodel Group {\n  id          String   @id @default(uuid())\n  name        String\n  description String?\n  owner_id    String\n  owner       User     @relation(fields: [owner_id], references: [id])\n  members     GroupMember[]\n  tasks       Task[]\n  created_at  DateTime @default(now())\n}\n\nmodel GroupMember {\n  id       String @id @default(uuid())\n  user_id  String\n  group_id String\n  user     User   @relation(fields: [user_id], references: [id])\n  group    Group  @relation(fields: [group_id], references: [id])\n  role     String @default("member")\n\n  @@unique([user_id, group_id])\n}\n\nmodel Task {\n  id          String   @id @default(uuid())\n  title       String\n  description String?\n  status      String   @default("todo")\n  priority    String   @default("medium")\n  group_id    String\n  group       Group    @relation(fields: [group_id], references: [id])\n  assigned_to String?\n  due_date    DateTime?\n  created_at  DateTime @default(now())\n}'
    },
    {
        "path": "backend/src/index.ts",
        "content": "import express from 'express';\nimport cors from 'cors';\nimport dotenv from 'dotenv';\n\ndotenv.config();\n\nconst app = express();\nconst PORT = process.env.PORT || 5000;\n\napp.use(cors());\napp.use(express.json());\n\napp.get('/', (req, res) => {\n  res.json({ message: 'GroupTaskHub API is running' });\n});\n\napp.listen(PORT, () => {\n  console.log(`Server is running on port ${PORT}`);\n});"
    },
    {
        "path": "frontend/package.json",
        "content": '{\n  "name": "grouptaskhub-frontend",\n  "version": "0.1.0",\n  "private": true,\n  "dependencies": {\n    "axios": "^1.6.8",\n    "react": "^18.2.0",\n    "react-dom": "^18.2.0",\n    "react-router-dom": "^6.22.3",\n    "lucide-react": "^0.372.0"\n  },\n  "scripts": {\n    "dev": "vite",\n    "build": "vite build",\n    "preview": "vite preview"\n  },\n  "devDependencies": {\n    "@types/react": "^18.2.66",\n    "@types/react-dom": "^18.2.22",\n    "@vitejs/plugin-react": "^4.2.1",\n    "autoprefixer": "^10.4.19",\n    "postcss": "^8.4.38",\n    "tailwindcss": "^3.4.3",\n    "typescript": "^5.2.2",\n    "vite": "^5.2.2"\n  }\n}'
    },
    {
        "path": "frontend/index.html",
        "content": '<!DOCTYPE html>\n<html lang="en">\n  <head>\n    <meta charset="UTF-8" />\n    <meta name="viewport" content="width=device-width, initial-scale=1.0" />\n    <title>GroupTaskHub</title>\n  </head>\n  <body>\n    <div id="root"></div>\n    <script type="module" src="/src/main.tsx"></script>\n  </body>\n</html>'
    }
]

base_dir = "E:\\file_rag\\grouptaskhub"
for f in files:
    full_path = os.path.join(base_dir, f["path"])
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w", encoding="utf-8") as file:
        file.write(f["content"])
    print(f"Created: {full_path}")
