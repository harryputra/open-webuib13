#!/bin/bash

mkdir -p /file_rag/si_tk
cd /file_rag/si_tk

# Create project structure
mkdir -p app/Http/{Controllers,Requests,Middleware} app/Models app/Providers
mkdir -p database/{migrations,seeders,factories}
mkdir -p resources/views/{layouts,components,auth,dashboard,master,transaksi,laporan}
mkdir -p public/{css,js,images,uploads/bukti_pembayaran,uploads/bukti_pengeluaran}
mkdir -p routes config storage/{app,framework,logs} tests bootstrap

# Create Laravel project files
cat > composer.json << 'EOF'
{
    "name": "yayasan/simkeu",
    "type": "project",
    "description": "Sistem Informasi Manajemen Keuangan Yayasan Pendidikan TK & SD Islam",
    "keywords": ["laravel", "accounting", "school", "finance"],
    "license": "MIT",
    "require": {
        "php": "^8.1",
        "guzzlehttp/guzzle": "^7.2",
        "laravel/framework": "^10.10",
        "laravel/sanctum": "^3.2",
        "laravel/tinker": "^2.8",
        "intervention/image": "^2.7",
        "maatwebsite/excel": "^3.1",
        "barryvdh/laravel-dompdf": "^2.0"
    },
    "require-dev": {
        "fakerphp/faker": "^1.9.1",
        "laravel/pint": "^1.0",
        "laravel/sail": "^1.18",
        "mockery/mockery": "^1.4.4",
        "nunomaduro/collision": "^7.0",
        "phpunit/phpunit": "^10.1",
        "spatie/laravel-ignition": "^2.0"
    },
    "autoload": {
        "psr-4": {
            "App\\": "app/",
            "Database\\Factories\\": "database/factories/",
            "Database\\Seeders\\": "database/seeders/"
        }
    },
    "extra": {
        "laravel": {
            "dont-discover": []
        }
    },
    "config": {
        "optimize-autoloader": true,
        "preferred-install": "dist",
        "sort-packages": true,
        "allow-plugins": {
            "pestphp/pest-plugin": true
        }
    },
    "scripts": {
        "post-autoload-dump": [
            "Illuminate\\Foundation\\ComposerScripts::postAutoloadDump",
            "@php artisan package:discover --ansi"
        ],
        "post-update-cmd": [
            "@php artisan vendor:publish --tag=laravel-assets --ansi --force"
        ],
        "post-root-package-install": [
            "@php -r \"file_exists('.env') || copy('.env.example', '.env');\""
        ],
        "post-create-package-install": [
            "@php -r \"file_exists('.env') || copy('.env.example', '.env');\""
        ]
    }
}
EOF

# Create .env file
cat > .env << 'EOF'
APP_NAME=SIMKEU_Yayasan
APP_ENV=local
APP_KEY=
APP_DEBUG=true
APP_URL=http://localhost:8000

LOG_CHANNEL=stack
LOG_DEPRECATIONS_CHANNEL=null
LOG_LEVEL=debug

DB_CONNECTION=mysql
DB_HOST=127.0.0.1
DB_PORT=3306
DB_DATABASE=simkeu_yayasan
DB_USERNAME=root
DB_PASSWORD=

BROADCAST_DRIVER=log
CACHE_DRIVER=file
FILESYSTEM_DISK=local
QUEUE_CONNECTION=sync
SESSION_DRIVER=file
SESSION_LIFETIME=120
EOF

# Create database migrations
cat > database/migrations/2024_01_01_000000_create_roles_table.php << 'EOF'
<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    public function up(): void
    {
        Schema::create('roles', function (Blueprint $table) {
            $table->id();
            $table->string('nama')->unique();
            $table->string('deskripsi')->nullable();
            $table->json('permissions')->nullable();
            $table->timestamps();
        });
    }

    public function down(): void
    {
        Schema::dropIfExists('roles');
    }
};
EOF

cat > database/migrations/2024_01_01_000001_create_users_table.php << 'EOF'
<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    public function up(): void
    {
        Schema::create('users', function (Blueprint $table) {
            $table->id();
            $table->string('username')->unique();
            $table->string('password');
            $table->string('nama');
            $table->foreignId('role_id')->constrained('roles');
            $table->rememberToken();
            $table->timestamps();
            $table->softDeletes();
        });
    }

    public function down(): void
    {
        Schema::dropIfExists('users');
    }
};
EOF

cat > database/migrations/2024_01_01_000002_create_tahun_ajaran_table.php << 'EOF'
<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    public function up(): void
    {
        Schema::create('tahun_ajaran', function (Blueprint $table) {
            $table->id();
            $table->string('tahun_ajaran', 9)->unique();
            $table->date('tanggal_mulai');
            $table->date('tanggal_selesai');
            $table->boolean('status_aktif')->default(false);
            $table->timestamps();
        });
    }

    public function down(): void
    {
        Schema::dropIfExists('tahun_ajaran');
    }
};
EOF

cat > database/migrations/2024_01_01_000003_create_kelas_table.php << 'EOF'
<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    public function up(): void
    {
        Schema::create('kelas', function (Blueprint $table) {
            $table->id();
            $table->string('nama_kelas');
            $table->string('tingkat');
            $table->string('wali_kelas')->nullable();
            $table->foreignId('tahun_ajaran_id')->constrained('tahun_ajaran');
            $table->timestamps();
        });
    }

    public function down(): void
    {
        Schema::dropIfExists('kelas');
    }
};
EOF

cat > database/migrations/2024_01_01_000004_create_siswa_table.php << 'EOF'
<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    public function up(): void
    {
        Schema::create('siswa', function (Blueprint $table) {
            $table->id();
            $table->string('nis')->unique();
            $table->string('nama');
            $table->foreignId('kelas_id')->constrained('kelas');
            $table->string('nama_ortu');
            $table->text('alamat')->nullable();
            $table->string('telp')->nullable();
            $table->enum('status', ['aktif', 'lulus', 'pindah'])->default('aktif');
            $table->timestamps();
            $table->softDeletes();
        });
    }

    public function down(): void
    {
        Schema::dropIfExists('siswa');
    }
};
EOF

cat > database/migrations/2024_01_01_000005_create_coa_table.php << 'EOF'
<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    public function up(): void
    {
        Schema::create('coa', function (Blueprint $table) {
            $table->id();
            $table->string('kode_akun', 10)->unique();
            $table->string('nama_akun');
            $table->enum('tipe', ['Aset', 'Kewajiban', 'Ekuitas', 'Pendapatan', 'Beban']);
            $table->enum('saldo_normal', ['Debit', 'Kredit']);
            $table->foreignId('parent_id')->nullable()->constrained('coa');
            $table->timestamps();
        });
    }

    public function down(): void
    {
        Schema::dropIfExists('coa');
    }
};
EOF

cat > database/migrations/2024_01_01_000006_create_jenis_tagihan_table.php << 'EOF'
<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    public function up(): void
    {
        Schema::create('jenis_tagihan', function (Blueprint $table) {
            $table->id();
            $table->string('nama');
            $table->text('deskripsi')->nullable();
            $table->foreignId('coa_pendapatan_id')->constrained('coa');
            $table->timestamps();
        });
    }

    public function down(): void
    {
        Schema::dropIfExists('jenis_tagihan');
    }
};
EOF

cat > database/migrations/2024_01_01_000007_create_tagihan_table.php << 'EOF'
<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    public function up(): void
    {
        Schema::create('tagihan', function (Blueprint $table) {
            $table->id();
            $table->foreignId('siswa_id')->constrained('siswa');
            $table->foreignId('jenis_tagihan_id')->constrained('jenis_tagihan');
            $table->foreignId('tahun_ajaran_id')->constrained('tahun_ajaran');
            $table->integer('bulan');
            $table->integer('tahun');
            $table->decimal('jumlah_tagihan', 15, 2);
            $table->enum('status', ['belum_lunas', 'lunas', 'cicilan'])->default('belum_lunas');
            $table->timestamps();
            
            $table->unique(['siswa_id', 'jenis_tagihan_id', 'bulan', 'tahun']);
        });
    }

    public function down(): void
    {
        Schema::dropIfExists('tagihan');
    }
};
EOF

cat > database/migrations/2024_01_01_000008_create_pembayaran_siswa_table.php << 'EOF'
<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    public function up(): void
    {
        Schema::create('pembayaran_siswa', function (Blueprint $table) {
            $table->id();
            $table->foreignId('tagihan_id')->constrained('tagihan');
            $table->decimal('jumlah_bayar', 15, 2);
            $table->date('tanggal');
            $table->enum('metode', ['tunai', 'transfer', 'lainnya']);
            $table->string('bukti_path')->nullable();
            $table->string('no_kuitansi')->unique();
            $table->foreignId('user_id')->constrained('users');
            $table->timestamps();
        });
    }

    public function down(): void
    {
        Schema::dropIfExists('pembayaran_siswa');
    }
};
EOF

cat > database/migrations/2024_01_01_000009_create_transaksi_table.php << 'EOF'
<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    public function up(): void
    {
        Schema::create('transaksi', function (Blueprint $table) {
            $table->id();
            $table->string('no_voucher')->unique();
            $table->date('tanggal');
            $table->enum('jenis', ['umum', 'pemasukan', 'pengeluaran', 'penyesuaian']);
            $table->text('keterangan');
            $table->foreignId('user_id')->constrained('users');
            $table->boolean('terkunci')->default(false);
            $table->timestamps();
        });
    }

    public function down(): void
    {
        Schema::dropIfExists('transaksi');
    }
};
EOF

cat > database/migrations/2024_01_01_000010_create_jurnal_detail_table.php << 'EOF'
<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    public function up(): void
    {
        Schema::create('jurnal_detail', function (Blueprint $table) {
            $table->id();
            $table->foreignId('transaksi_id')->constrained('transaksi');
            $table->foreignId('coa_id')->constrained('coa');
            $table->decimal('debit', 15, 2)->default(0);
            $table->decimal('kredit', 15, 2)->default(0);
            $table->timestamps();
        });
    }

    public function down(): void
    {
        Schema::dropIfExists('jurnal_detail');
    }
};
EOF

cat > database/migrations/2024_01_01_000011_create_pemasukan_lain_table.php << 'EOF'
<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    public function up(): void
    {
        Schema::create('pemasukan_lain', function (Blueprint $table) {
            $table->id();
            $table->foreignId('transaksi_id')->constrained('transaksi');
            $table->string('sumber_dana');
            $table->string('keterangan_tambahan')->nullable();
            $table->string('bukti_path')->nullable();
            $table->timestamps();
        });
    }

    public function down(): void
    {
        Schema::dropIfExists('pemasukan_lain');
    }
};
EOF

cat > database/migrations/2024_01_01_000012_create_pengeluaran_table.php << 'EOF'
<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    public function up(): void
    {
        Schema::create('pengeluaran', function (Blueprint $table) {
            $table->id();
            $table->foreignId('transaksi_id')->constrained('transaksi');
            $table->string('kategori');
            $table->string('penerima')->nullable();
            $table->string('keterangan_tambahan')->nullable();
            $table->string('bukti_path')->nullable();
            $table->timestamps();
        });
    }

    public function down(): void
    {
        Schema::dropIfExists('pengeluaran');
    }
};
EOF

cat > database/migrations/2024_01_01_000013_create_audit_log_table.php << 'EOF'
<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    public function up(): void
    {
        Schema::create('audit_log', function (Blueprint $table) {
            $table->id();
            $table->string('table_name');
            $table->string('action');
            $table->json('old_data')->nullable();
            $table->json('new_data')->nullable();
            $table->foreignId('user_id')->constrained('users');
            $table->timestamps();
        });
    }

    public function down(): void
    {
        Schema::dropIfExists('audit_log');
    }
};
EOF

cat > app/Models/Role.php << 'EOF'
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\HasMany;

class Role extends Model
{
    use HasFactory;

    protected $table = 'roles';
    protected $fillable = ['nama', 'deskripsi', 'permissions'];
    protected $casts = ['permissions' => 'array'];

    public function users(): HasMany
    {
        return $this->hasMany(User::class);
    }
}
EOF

cat > app/Models/User.php << 'EOF'
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\SoftDeletes;
use Illuminate\Foundation\Auth\User as Authenticatable;
use Illuminate\Notifications\Notifiable;
use Illuminate\Database\Eloquent\Relations\BelongsTo;
use Illuminate\Database\Eloquent\Relations\HasMany;

class User extends Authenticatable
{
    use HasFactory, Notifiable, SoftDeletes;

    protected $table = 'users';
    protected $fillable = ['username', 'password', 'nama', 'role_id'];
    protected $hidden = ['password', 'remember_token'];
    protected $casts = ['email_verified_at' => 'datetime'];

    public function role(): BelongsTo
    {
        return $this->belongsTo(Role::class);
    }

    public function transaksi(): HasMany
    {
        return $this->hasMany(Transaksi::class);
    }

    public function pembayaranSiswa(): HasMany
    {
        return $this->hasMany(PembayaranSiswa::class);
    }

    public function hasPermission($permission): bool
    {
        return in_array($permission, $this->role->permissions ?? []);
    }
}
EOF

cat > app/Models/TahunAjaran.php << 'EOF'
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\HasMany;

class TahunAjaran extends Model
{
    use HasFactory;

    protected $table = 'tahun_ajaran';
    protected $fillable = ['tahun_ajaran', 'tanggal_mulai', 'tanggal_selesai', 'status_aktif'];

    public function kelas(): HasMany
    {
        return $this->hasMany(Kelas::class);
    }

    public function tagihan(): HasMany
    {
        return $this->hasMany(Tagihan::class);
    }
}
EOF

cat > app/Models/Kelas.php << 'EOF'
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;
use Illuminate\Database\Eloquent\Relations\HasMany;

class Kelas extends Model
{
    use HasFactory;

    protected $table = 'kelas';
    protected $fillable = ['nama_kelas', 'tingkat', 'wali_kelas', 'tahun_ajaran_id'];

    public function tahunAjaran(): BelongsTo
    {
        return $this->belongsTo(TahunAjaran::class);
    }

    public function siswa(): HasMany
    {
        return $this->hasMany(Siswa::class);
    }
}
EOF

cat > app/Models/Siswa.php << 'EOF'
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\SoftDeletes;
use Illuminate\Database\Eloquent\Relations\BelongsTo;
use Illuminate\Database\Eloquent\Relations\HasMany;

class Siswa extends Model
{
    use HasFactory, SoftDeletes;

    protected $table = 'siswa';
    protected $fillable = ['nis', 'nama', 'kelas_id', 'nama_ortu', 'alamat', 'telp', 'status'];

    public function kelas(): BelongsTo
    {
        return $this->belongsTo(Kelas::class);
    }

    public function tagihan(): HasMany
    {
        return $this->hasMany(Tagihan::class);
    }

    public function pembayaranSiswa(): HasMany
    {
        return $this->hasManyThrough(PembayaranSiswa::class, Tagihan::class);
    }
}
EOF

cat > app/Models/COA.php << 'EOF'
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;
use Illuminate\Database\Eloquent\Relations\HasMany;

class COA extends Model
{
    use HasFactory;

    protected $table = 'coa';
    protected $fillable = ['kode_akun', 'nama_akun', 'tipe', 'saldo_normal', 'parent_id'];

    public function parent(): BelongsTo
    {
        return $this->belongsTo(COA::class, 'parent_id');
    }

    public function children(): HasMany
    {
        return $this->hasMany(COA::class, 'parent_id');
    }

    public function jurnalDetail(): HasMany
    {
        return $this->hasMany(JurnalDetail::class);
    }

    public function getSaldoAttribute()
    {
        $debit = $this->jurnalDetail()->sum('debit');
        $kredit = $this->jurnalDetail()->sum('kredit');
        
        return $this->saldo_normal === 'Debit' ? $debit - $kredit : $kredit - $debit;
    }
}
EOF

cat > app/Models/JenisTagihan.php << 'EOF'
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;
use Illuminate\Database\Eloquent\Relations\HasMany;

class JenisTagihan extends Model
{
    use HasFactory;

    protected $table = 'jenis_tagihan';
    protected $fillable = ['nama', 'deskripsi', 'coa_pendapatan_id'];

    public function coaPendapatan(): BelongsTo
    {
        return $this->belongsTo(COA::class, 'coa_pendapatan_id');
    }

    public function tagihan(): HasMany
    {
        return $this->hasMany(Tagihan::class);
    }
}
EOF

cat > app/Models/Tagihan.php << 'EOF'
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;
use Illuminate\Database\Eloquent\Relations\HasMany;

class Tagihan extends Model
{
    use HasFactory;

    protected $table = 'tagihan';
    protected $fillable = ['siswa_id', 'jenis_tagihan_id', 'tahun_ajaran_id', 'bulan', 'tahun', 'jumlah_tagihan', 'status'];

    public function siswa(): BelongsTo
    {
        return $this->belongsTo(Siswa::class);
    }

    public function jenisTagihan(): BelongsTo
    {
        return $this->belongsTo(JenisTagihan::class);
    }

    public function tahunAjaran(): BelongsTo
    {
        return $this->belongsTo(TahunAjaran::class);
    }

    public function pembayaranSiswa(): HasMany
    {
        return $this->hasMany(PembayaranSiswa::class);
    }

    public function getTerbayarAttribute()
    {
        return $this->pembayaranSiswa()->sum('jumlah_bayar');
    }

    public function getSisaAttribute()
    {
        return $this->jumlah_tagihan - $this->terbayar;
    }

    public function updateStatus()
    {
        if ($this->terbayar >= $this->jumlah_tagihan) {
            $this->status = 'lunas';
        } elseif ($this->terbayar > 0) {
            $this->status = 'cicilan';
        } else {
            $this->status = 'belum_lunas';
        }
        $this->save();
    }
}
EOF

cat > app/Models/PembayaranSiswa.php << 'EOF'
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;

class PembayaranSiswa extends Model
{
    use HasFactory;

    protected $table = 'pembayaran_siswa';
    protected $fillable = ['tagihan_id', 'jumlah_bayar', 'tanggal', 'metode', 'bukti_path', 'no_kuitansi', 'user_id'];

    public function tagihan(): BelongsTo
    {
        return $this->belongsTo(Tagihan::class);
    }

    public function user(): BelongsTo
    {
        return $this->belongsTo(User::class);
    }

    protected static function boot()
    {
        parent::boot();

        static::creating(function ($model) {
            $model->no_kuitansi = 'KUIT-' . date('Ymd') . '-' . str_pad(self::whereDate('created_at', today())->count() + 1, 4, '0', STR_PAD_LEFT);
        });

        static::created(function ($model) {
            $model->tagihan->updateStatus();
        });
    }
}
EOF

cat > app/Models/Transaksi.php << 'EOF'
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;
use Illuminate\Database\Eloquent\Relations\HasMany;

class Transaksi extends Model
{
    use HasFactory;

    protected $table = 'transaksi';
    protected $fillable = ['no_voucher', 'tanggal', 'jenis', 'keterangan', 'user_id', 'terkunci'];

    public function user(): BelongsTo
    {
        return $this->belongsTo(User::class);
    }

    public function jurnalDetail(): HasMany
    {
        return $this->hasMany(JurnalDetail::class);
    }

    public function pemasukanLain(): HasOne
    {
        return $this->hasOne(PemasukanLain::class);
    }

    public function pengeluaran(): HasOne
    {
        return $this->hasOne(Pengeluaran::class);
    }

    protected static function boot()
    {
        parent::boot();

        static::creating(function ($model) {
            if (empty($model->no_voucher)) {
                $count = self::whereDate('created_at', today())->count() + 1;
                $model->no_voucher = 'VCH-' . date('Ymd') . '-' . str_pad($count, 4, '0', STR_PAD_LEFT);
            }
        });
    }

    public function getTotalDebitAttribute()
    {
        return $this->jurnalDetail->sum('debit');
    }

    public function getTotalKreditAttribute()
    {
        return $this->jurnalDetail->sum('kredit');
    }

    public function isBalanced()
    {
        return $this->total_debit === $this->total_kredit;
    }
}
EOF

cat > app/Models/JurnalDetail.php << 'EOF'
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;

class JurnalDetail extends Model
{
    use HasFactory;

    protected $table = 'jurnal_detail';
    protected $fillable = ['transaksi_id', 'coa_id', 'debit', 'kredit'];

    public function transaksi(): BelongsTo
    {
        return $this->belongsTo(Transaksi::class);
    }

    public function coa(): BelongsTo
    {
        return $this->belongsTo(COA::class);
    }
}
EOF

cat > app/Models/PemasukanLain.php << 'EOF'
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;

class PemasukanLain extends Model
{
    use HasFactory;

    protected $table = 'pemasukan_lain';
    protected $fillable = ['transaksi_id', 'sumber_dana', 'keterangan_tambahan', 'bukti_path'];

    public function transaksi(): BelongsTo
    {
        return $this->belongsTo(Transaksi::class);
    }
}
EOF

cat > app/Models/Pengeluaran.php << 'EOF'
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;

class Pengeluaran extends Model
{
    use HasFactory;

    protected $table = 'pengeluaran';
    protected $fillable = ['transaksi_id', 'kategori', 'penerima', 'keterangan_tambahan', 'bukti_path'];

    public function transaksi(): BelongsTo
    {
        return $this->belongsTo(Transaksi::class);
    }
}
EOF

cat > app/Models/AuditLog.php << 'EOF'
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;

class AuditLog extends Model
{
    use HasFactory;

    protected $table = 'audit_log';
    protected $fillable = ['table_name', 'action', 'old_data', 'new_data', 'user_id'];
    protected $casts = ['old_data' => 'json', 'new_data' => 'json'];

    public function user(): BelongsTo
    {
        return $this->belongsTo(User::class);
    }
}
EOF

cat > app/Http/Controllers/AuthController.php << 'EOF'
<?php

namespace App\Http\Controllers;

use App\Models\User;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Auth;
use Illuminate\Support\Facades\Hash;
use Illuminate\Support\Facades\Validator;

class AuthController extends Controller
{
    public function showLogin()
    {
        return view('auth.login');
    }

    public function login(Request $request)
    {
        $validator = Validator::make($request->all(), [
            'username' => 'required',
            'password' => 'required'
        ]);

        if ($validator->fails()) {
            return redirect()->back()->withErrors($validator)->withInput();
        }

        $credentials = $request->only('username', 'password');
        
        if (Auth::attempt($credentials)) {
            $request->session()->regenerate();
            return redirect()->intended('/dashboard');
        }

        return back()->withErrors([
            'username' => 'Username atau password salah.',
        ])->withInput();
    }

    public function logout(Request $request)
    {
        Auth::logout();
        $request->session()->invalidate();
        $request->session()->regenerateToken();
        return redirect('/login');
    }

    public function showProfile()
    {
        return view('auth.profile');
    }

    public function updateProfile(Request $request)
    {
        $user = Auth::user();
        
        $validator = Validator::make($request->all(), [
            'nama' => 'required|string|max:255',
            'password' => 'nullable|min:6|confirmed'
        ]);

        if ($validator->fails()) {
            return redirect()->back()->withErrors($validator)->withInput();
        }

        $user->nama = $request->nama;
        
        if ($request->filled('password')) {
            $user->password = Hash::make($request->password);
        }

        $user->save();

        return redirect()->back()->with('success', 'Profil berhasil diperbarui.');
    }
}
EOF

cat > app/Http/Controllers/DashboardController.php << 'EOF'
<?php

namespace App\Http\Controllers;

use App\Models\COA;
use App\Models\Tagihan;
use App\Models\Transaksi;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\DB;

class DashboardController extends Controller
{
    public function index()
    {
        $totalSiswaAktif = DB::table('siswa')->where('status', 'aktif')->count();
        $totalTagihanBulanIni = Tagihan::where('bulan', date('n'))->where('tahun', date('Y'))->sum('jumlah_tagihan');
        $totalTerbayarBulanIni = DB::table('pembayaran_siswa')
            ->whereMonth('tanggal', date('n'))
            ->whereYear('tanggal', date('Y'))
            ->sum('jumlah_bayar');
        
        $saldoKas = COA::where('kode_akun', 'like', '1-1%')->get()->sum('saldo');
        $saldoBank = COA::where('kode_akun', 'like', '1-2%')->get()->sum('saldo');

        $tunggakan = DB::table('tagihan')
            ->where('status', '!=', 'lunas')
            ->sum(DB::raw('jumlah_tagihan - (
                SELECT COALESCE(SUM(jumlah_bayar), 0) 
                FROM pembayaran_siswa 
                WHERE pembayaran_siswa.tagihan_id = tagihan.id
            )'));

        $transaksiTerbaru = Transaksi::with('jurnalDetail.coa')
            ->orderBy('created_at', 'desc')
            ->take(10)
            ->get();

        $chartData = $this->getChartData();

        return view('dashboard.index', compact(
            'totalSiswaAktif',
            'totalTagihanBulanIni',
            'totalTerbayarBulanIni',
            'saldoKas',
            'saldoBank',
            'tunggakan',
            'transaksiTerbaru',
            'chartData'
        ));
    }

    private function getChartData()
    {
        $data = DB::table('pembayaran_siswa')
            ->select(
                DB::raw('MONTH(tanggal) as bulan'),
                DB::raw('YEAR(tanggal) as tahun'),
                DB::raw('SUM(jumlah_bayar) as total')
            )
            ->whereYear('tanggal', date('Y'))
            ->groupBy('tahun', 'bulan')
            ->orderBy('tahun')
            ->orderBy('bulan')
            ->get();

        $months = [];
        $totals = [];

        for ($i = 1; $i <= 12; $i++) {
            $months[] = date('M', mktime(0, 0, 0, $i, 1));
            $monthData = $data->where('bulan', $i)->first();
            $totals[] = $monthData ? $monthData->total : 0;
        }

        return [
            'months' => $months,
            'totals' => $totals
        ];
    }
}
EOF

cat > resources/views/layouts/app.blade.php << 'EOF'
<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SIMKEU - {{ $title ?? 'Dashboard' }}</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <link href="https://cdn.jsdelivr.net/npm/admin-lte@3.2/dist/css/adminlte.min.css" rel="stylesheet">
    <style>
        .sidebar-dark-primary {
            background-color: #00695c !important;
        }
        .navbar-dark {
            background-color: #004d40 !important;
        }
    </style>
</head>
<body class="hold-transition sidebar-mini layout-fixed">
<div class="wrapper">

    <!-- Navbar -->
    <nav class="main-header navbar navbar-expand navbar-dark">
        <!-- Left navbar links -->
        <ul class="navbar-nav">
            <li class="nav-item">
                <a class="nav-link" data-widget="pushmenu" href="#" role="button"><i class="fas fa-bars"></i></a>
            </li>
        </ul>

        <!-- Right navbar links -->
        <ul class="navbar-nav ml-auto">
            <li class="nav-item dropdown">
                <a class="nav-link" data-toggle="dropdown" href="#">
                    <i class="fas fa-user"></i> {{ Auth::user()->nama }}
                </a>
                <div class="dropdown-menu dropdown-menu-right">
                    <a href="{{ route('profile') }}" class="dropdown-item">
                        <i class="fas fa-user mr-2"></i> Profil
                    </a>
                    <div class="dropdown-divider"></div>
                    <form method="POST" action="{{ route('logout') }}">
                        @csrf
                        <button type="submit" class="dropdown-item">
                            <i class="fas fa-sign-out-alt mr-2"></i> Logout
                        </button>
                    </form>
                </div>
            </li>
        </ul>
    </nav>

    <!-- Main Sidebar Container -->
    <aside class="main-sidebar sidebar-dark-primary elevation-4">
        <!-- Brand Logo -->
        <a href="{{ route('dashboard') }}" class="brand-link text-center">
            <span class="brand-text font-weight-light">SIMKEU YAYASAN</span>
        </a>

        <!-- Sidebar -->
        <div class="sidebar">
            <!-- Sidebar Menu -->
            <nav class="mt-2">
                <ul class="nav nav-pills nav-sidebar flex-column" data-widget="treeview" role="menu">
                    <li class="nav-item">
                        <a href="{{ route('dashboard') }}" class="nav-link {{ request()->is('dashboard') ? 'active' : '' }}">
                            <i class="nav-icon fas fa-tachometer-alt"></i>
                            <p>Dashboard</p>
                        </a>
                    </li>

                    @if(Auth::user()->hasPermission('master_data'))
                    <li class="nav-item">
                        <a href="#" class="nav-link">
                            <i class="nav-icon fas fa-database"></i>
                            <p>Master Data <i class="right fas fa-angle-left"></i></p>
                        </a>
                        <ul class="nav nav-treeview">
                            <li class="nav-item">
                                <a href="{{ route('tahun-ajaran.index') }}" class="nav-link">
                                    <i class="fas fa-calendar nav-icon"></i>
                                    <p>Tahun Ajaran</p>
                                </a>
                            </li>
                            <li class="nav-item">
                                <a href="{{ route('kelas.index') }}" class="nav-link">
                                    <i class="fas fa-chalkboard nav-icon"></i>
                                    <p>Kelas</p>
                                </a>
                            </li>
                            <li class="nav-item">
                                <a href="{{ route('siswa.index') }}" class="nav-link">
                                    <i class="fas fa-user-graduate nav-icon"></i>
                                    <p>Siswa</p>
                                </a>
                            </li>
                            <li class="nav-item">
                                <a href="{{ route('coa.index') }}" class="nav-link">
                                    <i class="fas fa-chart-pie nav-icon"></i>
                                    <p>Chart of Accounts</p>
                                </a>
                            </li>
                        </ul>
                    </li>
                    @endif

                    <li class="nav-item">
                        <a href="{{ route('tagihan.index') }}" class="nav-link {{ request()->is('tagihan*') ? 'active' : '' }}">
                            <i class="nav-icon fas fa-file-invoice-dollar"></i>
                            <p>Tagihan Siswa</p>
                        </a>
                    </li>

                    <li class="nav-item">
                        <a href="{{ route('pembayaran.index') }}" class="nav-link {{ request()->is('pembayaran*') ? 'active' : '' }}">
                            <i class="nav-icon fas fa-cash-register"></i>
                            <p>Pembayaran</p>
                        </a>
                    </li>

                    <li class="nav-item">
                        <a href="{{ route('transaksi.index') }}" class="nav-link {{ request()->is('transaksi*') ? 'active' : '' }}">
                            <i class="nav-icon fas fa-book"></i>
                            <p>Jurnal</p>
                        </a>
                    </li>

                    <li class="nav-item">
                        <a href="{{ route('laporan.index') }}" class="nav-link {{ request()->is('laporan*') ? 'active' : '' }}">
                            <i class="nav-icon fas fa-chart-bar"></i>
                            <p>Laporan</p>
                        </a>
                    </li>

                    @if(Auth::user()->hasPermission('user_management'))
                    <li class="nav-item">
                        <a href="{{ route('users.index') }}" class="nav-link {{ request()->is('users*') ? 'active' : '' }}">
                            <i class="nav-icon fas fa-users"></i>
                            <p>Manajemen User</p>
                        </a>
                    </li>
                    @endif
                </ul>
            </nav>
        </div>
    </aside>

    <!-- Content Wrapper. Contains page content -->
    <div class="content-wrapper">
        <!-- Content Header (Page header) -->
        <div class="content-header">
            <div class="container-fluid">
                <div class="row mb-2">
                    <div class="col-sm-6">
                        <h1 class="m-0">{{ $title ?? 'Dashboard' }}</h1>
                    </div>
                    <div class="col-sm-6">
                        <ol class="breadcrumb float-sm-right">
                            <li class="breadcrumb-item"><a href="{{ route('dashboard') }}">Home</a></li>
                            <li class="breadcrumb-item active">{{ $title ?? 'Dashboard' }}</li>
                        </ol>
                    </div>
                </div>
            </div>
        </div>

        <!-- Main content -->
        <section class="content">
            <div class="container-fluid">
                @if(session('success'))
                    <div class="alert alert-success alert-dismissible">
                        <button type="button" class="close" data-dismiss="alert" aria-hidden="true">×</button>
                        <i class="icon fas fa-check"></i> {{ session('success') }}
                    </div>
                @endif

                @if(session('error'))
                    <div class="alert alert-danger alert-dismissible">
                        <button type="button" class="close" data-dismiss="alert" aria-hidden="true">×</button>
                        <i class="icon fas fa-ban"></i> {{ session('error') }}
                    </div>
                @endif

                @yield('content')
            </div>
        </section>
    </div>

    <!-- Footer -->
    <footer class="main-footer">
        <strong>SIMKEU Yayasan &copy; 2024</strong>
        <div class="float-right d-none d-sm-inline-block">
            <b>Version</b> 1.0.0
        </div>
    </footer>
</div>

<script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/admin-lte@3.2/dist/js/adminlte.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
@stack('scripts')
</body>
</html>
EOF

cat > resources/views/dashboard/index.blade.php << 'EOF'
@extends('layouts.app')

@section('title', 'Dashboard')

@section('content')
<div class="row">
    <!-- Saldo Kas -->
    <div class="col-lg-3 col-6">
        <div class="small-box bg-info">
            <div class="inner">
                <h3>Rp {{ number_format($saldoKas, 0, ',', '.') }}</h3>
                <p>Saldo Kas</p>
            </div>
            <div class="icon">
                <i class="fas fa-wallet"></i>
            </div>
            <a href="{{ route('transaksi.index') }}" class="small-box-footer">More info <i class="fas fa-arrow-circle-right"></i></a>
        </div>
    </div>

    <!-- Saldo Bank -->
    <div class="col-lg-3 col-6">
        <div class="small-box bg-success">
            <div class="inner">
                <h3>Rp {{ number_format($saldoBank, 0, ',', '.') }}</h3>
                <p>Saldo Bank</p>
            </div>
            <div class="icon">
                <i class="fas fa-building"></i>
            </div>
            <a href="{{ route('transaksi.index') }}" class="small-box-footer">More info <i class="fas fa-arrow-circle-right"></i></a>
        </div>
    </div>

    <!-- Total Tunggakan -->
    <div class="col-lg-3 col-6">
        <div class="small-box bg-warning">
            <div class="inner">
                <h3>Rp {{ number_format($tunggakan, 0, ',', '.') }}</h3>
                <p>Total Tunggakan</p>
            </div>
            <div class="icon">
                <i class="fas fa-exclamation-triangle"></i>
            </div>
            <a href="{{ route('tagihan.index') }}" class="small-box-footer">More info <i class="fas fa-arrow-circle-right"></i></a>
        </div>
    </div>

    <!-- Total Siswa Aktif -->
    <div class="col-lg-3 col-6">
        <div class="small-box bg-primary">
            <div class="inner">
                <h3>{{ number_format($totalSiswaAktif, 0, ',', '.') }}</h3>
                <p>Siswa Aktif</p>
            </div>
            <div class="icon">
                <i class="fas fa-users"></i>
            </div>
            <a href="{{ route('siswa.index') }}" class="small-box-footer">More info <i class="fas fa-arrow-circle-right"></i></a>
        </div>
    </div>
</div>

<div class="row">
    <div class="col-md-8">
        <div class="card">
            <div class="card-header">
                <h3 class="card-title">Pendapatan Bulanan</h3>
            </div>
            <div class="card-body">
                <canvas id="revenueChart" style="min-height: 250px; height: 250px; max-height: 250px; max-width: 100%;"></canvas>
            </div>
        </div>
    </div>

    <div class="col-md-4">
        <div class="card">
            <div class="card-header">
                <h3 class="card-title">Transaksi Terbaru</h3>
            </div>
            <div class="card-body p-0">
                <ul class="products-list product-list-in-card pl-2 pr-2">
                    @foreach($transaksiTerbaru as $transaksi)
                    <li class="item">
                        <div class="product-info">
                            <a href="javascript:void(0)" class="product-title">
                                {{ $transaksi->no_voucher }}
                                <span class="badge badge-{{ $transaksi->jenis == 'pemasukan' ? 'success' : 'warning' }} float-right">
                                    Rp {{ number_format($transaksi->total_debit, 0, ',', '.') }}
                                </span>
                            </a>
                            <span class="product-description">
                                {{ $transaksi->keterangan }}<br>
                                <small>{{ $transaksi->tanggal->format('d M Y') }}</small>
                            </span>
                        </div>
                    </li>
                    @endforeach
                </ul>
            </div>
        </div>
    </div>
</div>

<div class="row">
    <div class="col-12">
        <div class="card">
            <div class="card-header">
                <h3 class="card-title">Ringkasan Bulan Ini</h3>
            </div>
            <div class="card-body">
                <div class="row">
                    <div class="col-md-6">
                        <div class="info-box bg-light">
                            <span class="info-box-icon bg-info"><i class="fas fa-file-invoice-dollar"></i></span>
                            <div class="info-box-content">
                                <span class="info-box-text">Total Tagihan Bulan Ini</span>
                                <span class="info-box-number">Rp {{ number_format($totalTagihanBulanIni, 0, ',', '.') }}</span>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-6">
                        <div class="info-box bg-light">
                            <span class="info-box-icon bg-success"><i class="fas fa-money-bill-wave"></i></span>
                            <div class="info-box-content">
                                <span class="info-box-text">Total Terbayar Bulan Ini</span>
                                <span class="info-box-number">Rp {{ number_format($totalTerbayarBulanIni, 0, ',', '.') }}</span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
@endsection

@push('scripts')
<script>
$(function () {
    var revenueChart = new Chart($('#revenueChart'), {
        type: 'bar',
        data: {
            labels: @json($chartData['months']),
            datasets: [{
                label: 'Pendapatan',
                backgroundColor: 'rgba(60,141,188,0.9)',
                borderColor: 'rgba(60,141,188,0.8)',
                pointRadius: false,
                pointColor: '#3b8bba',
                pointStrokeColor: 'rgba(60,141,188,1)',
                pointHighlightFill: '#fff',
                pointHighlightStroke: 'rgba(60,141,188,1)',
                data: @json($chartData['totals'])
            }]
        },
        options: {
            maintainAspectRatio: false,
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        callback: function(value) {
                            return 'Rp ' + value.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ".");
                        }
                    }
                }
            },
            plugins: {
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            return 'Rp ' + context.raw.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ".");
                        }
                    }
                }
            }
        }
    });
});
</script>
@endpush
EOF

cat > resources/views/auth/login.blade.php << 'EOF'
<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Login - SIMKEU Yayasan</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <style>
        body {
            background: linear-gradient(135deg, #00695c 0%, #004d40 100%);
            height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .login-box {
            background: white;
            border-radius: 10px;
            box-shadow: 0 0 20px rgba(0,0,0,0.1);
            width: 400px;
            max-width: 90%;
        }
        .login-logo {
            text-align: center;
            padding: 20px;
            background: #00695c;
            border-radius: 10px 10px 0 0;
            color: white;
        }
    </style>
</head>
<body>
    <div class="login-box">
        <div class="login-logo">
            <h2><i class="fas fa-calculator"></i> SIMKEU YAYASAN</h2>
            <p>Sistem Informasi Manajemen Keuangan</p>
        </div>
        <div class="card-body">
            <form method="POST" action="{{ route('login') }}">
                @csrf
                <div class="mb-3">
                    <label for="username" class="form-label">Username</label>
                    <input type="text" class="form-control @error('username') is-invalid @enderror" 
                           id="username" name="username" value="{{ old('username') }}" required autofocus>
                    @error('username')
                        <div class="invalid-feedback">{{ $message }}</div>
                    @enderror
                </div>
                <div class="mb-3">
                    <label for="password" class="form-label">Password</label>
                    <input type="password" class="form-control @error('password') is-invalid @enderror" 
                           id="password" name="password" required>
                    @error('password')
                        <div class="invalid-feedback">{{ $message }}</div>
                    @enderror
                </div>
                <button type="submit" class="btn btn-primary w-100">
                    <i class="fas fa-sign-in-alt"></i> Login
                </button>
            </form>
            @if(session('error'))
                <div class="alert alert-danger mt-3">
                    <i class="fas fa-exclamation-triangle"></i> {{ session('error') }}
                </div>
            @endif
        </div>
    </div>

    <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
EOF

cat > routes/web.php << 'EOF'
<?php

use Illuminate\Support\Facades\Route;
use App\Http\Controllers\AuthController;
use App\Http\Controllers\DashboardController;

// Authentication Routes
Route::get('/login', [AuthController::class, 'showLogin'])->name('login');
Route::post('/login', [AuthController::class, 'login']);
Route::post('/logout', [AuthController::class, 'logout'])->name('logout');

// Protected Routes
Route::middleware(['auth'])->group(function () {
    // Dashboard
    Route::get('/dashboard', [DashboardController::class, 'index'])->name('dashboard');
    Route::get('/', function () { return redirect('/dashboard'); });

    // Profile
    Route::get('/profile', [AuthController::class, 'showProfile'])->name('profile');
    Route::post('/profile', [AuthController::class, 'updateProfile']);

    // Master Data Routes (will be added later)
    Route::prefix('master')->group(function () {
        // Tahun Ajaran, Kelas, Siswa, COA routes will be added here
    });

    // Transaction Routes (will be added later)
    Route::prefix('transaksi')->group(function () {
        // Tagihan, Pembayaran, Jurnal routes will be added here
    });

    // Report Routes (will be added later)
    Route::prefix('laporan')->group(function () {
        // Various report routes will be added here
    });
});
EOF

cat > index.php << 'EOF'
<?php

use Illuminate\Foundation\Application;
use Illuminate\Http\Request;

define('LARAVEL_START', microtime(true));

// Determine if the application is in maintenance mode...
if (file_exists($maintenance = __DIR__.'/storage/framework/maintenance.php')) {
    require $maintenance;
}

// Register the Composer autoloader...
require __DIR__.'/vendor/autoload.php';

// Bootstrap Laravel and handle the request...
$app = require_once __DIR__.'/bootstrap/app.php';

$kernel = $app->make(Illuminate\Contracts\Http\Kernel::class);

$response = $kernel->handle(
    $request = Request::capture()
);

$response->send();

$kernel->terminate($request, $response);
EOF

cat > bootstrap/app.php << 'EOF'
<?php

require_once __DIR__.'/../vendor/autoload.php';

$app = new Illuminate\Foundation\Application(
    $_ENV['APP_BASE_PATH'] ?? dirname(__DIR__)
);

$app->singleton(
    Illuminate\Contracts\Http\Kernel::class,
    App\Http\Kernel::class
);

$app->singleton(
    Illuminate\Contracts\Console\Kernel::class,
    App\Console\Kernel::class
);

$app->singleton(
    Illuminate\Contracts\Debug\ExceptionHandler::class,
    App\Exceptions\Handler::class
);

return $app;
EOF

cat > app/Http/Kernel.php << 'EOF'
<?php

namespace App\Http;

use Illuminate\Foundation\Http\Kernel as HttpKernel;

class Kernel extends HttpKernel
{
    protected $middleware = [
        \App\Http\Middleware\TrustProxies::class,
        \Illuminate\Http\Middleware\HandleCors::class,
        \App\Http\Middleware\PreventRequestsDuringMaintenance::class,
        \Illuminate\Foundation\Http\Middleware\ValidatePostSize::class,
        \App\Http\Middleware\TrimStrings::class,
        \Illuminate\Foundation\Http\Middleware\ConvertEmptyStringsToNull::class,
    ];

    protected $middlewareGroups = [
        'web' => [
            \App\Http\Middleware\EncryptCookies::class,
            \Illuminate\Cookie\Middleware\AddQueuedCookiesToResponse::class,
            \Illuminate\Session\Middleware\StartSession::class,
            \Illuminate\View\Middleware\ShareErrorsFromSession::class,
            \App\Http\Middleware\VerifyCsrfToken::class,
            \Illuminate\Routing\Middleware\SubstituteBindings::class,
        ],

        'api' => [
            \Laravel\Sanctum\Http\Middleware\EnsureFrontendRequestsAreStateful::class,
            'throttle:api',
            \Illuminate\Routing\Middleware\SubstituteBindings::class,
        ],
    ];

    protected $middlewareAliases = [
        'auth' => \App\Http\Middleware\Authenticate::class,
        'auth.basic' => \Illuminate\Auth\Middleware\AuthenticateWithBasicAuth::class,
        'auth.session' => \Illuminate\Session\Middleware\AuthenticateSession::class,
        'cache.headers' => \Illuminate\Http\Middleware\SetCacheHeaders::class,
        'can' => \Illuminate\Auth\Middleware\Authorize::class,
        'guest' => \App\Http\Middleware\RedirectIfAuthenticated::class,
        'password.confirm' => \Illuminate\Auth\Middleware\RequirePassword::class,
        'signed' => \Illuminate\Routing\Middleware\ValidateSignature::class,
        'throttle' => \Illuminate\Routing\Middleware\ThrottleRequests::class,
        'verified' => \Illuminate\Auth\Middleware\EnsureEmailIsVerified::class,
    ];
}
EOF

cat > app/Http/Middleware/Authenticate.php << 'EOF'
<?php

namespace App\Http\Middleware;

use Illuminate\Auth\Middleware\Authenticate as Middleware;
use Illuminate\Http\Request;

class Authenticate extends Middleware
{
    protected function redirectTo(Request $request): ?string
    {
        return $request->expectsJson() ? null : route('login');
    }
}
EOF

cat > app/Http/Middleware/EncryptCookies.php << 'EOF'
<?php

namespace App\Http\Middleware;

use Illuminate\Cookie\Middleware\EncryptCookies as Middleware;

class EncryptCookies extends Middleware
{
    protected $except = [];
}
EOF

cat > app/Http/Middleware/VerifyCsrfToken.php << 'EOF'
<?php

namespace App\Http\Middleware;

use Illuminate\Foundation\Http\Middleware\VerifyCsrfToken as Middleware;

class VerifyCsrfToken extends Middleware
{
    protected $except = [];
}
EOF

cat > database/seeders/DatabaseSeeder.php << 'EOF'
<?php

namespace Database\Seeders;

use Illuminate\Database\Seeder;
use App\Models\Role;
use App\Models\User;
use App\Models\COA;
use Illuminate\Support\Facades\Hash;

class DatabaseSeeder extends Seeder
{
    public function run(): void
    {
        // Seed Roles
        $roles = [
            ['nama' => 'Administrator', 'deskripsi' => 'Super admin dengan akses penuh'],
            ['nama' => 'Bendahara', 'deskripsi' => 'Staff keuangan yang menginput transaksi'],
            ['nama' => 'Kepala Yayasan', 'deskripsi' => 'Pimpinan yayasan yang melihat laporan'],
            ['nama' => 'Auditor', 'deskripsi' => 'Auditor internal yang memeriksa data'],
        ];

        foreach ($roles as $role) {
            Role::create($role);
        }

        // Seed Admin User
        User::create([
            'username' => 'admin',
            'password' => Hash::make('password'),
            'nama' => 'Administrator System',
            'role_id' => 1,
        ]);

        // Seed Chart of Accounts
        $coaData = [
            // Aset
            ['kode_akun' => '1-1000', 'nama_akun' => 'Kas Tunai', 'tipe' => 'Aset', 'saldo_normal' => 'Debit'],
            ['kode_akun' => '1-2000', 'nama_akun' => 'Bank BSI', 'tipe' => 'Aset', 'saldo_normal' => 'Debit'],
            ['kode_akun' => '1-3000', 'nama_akun' => 'Piutang SPP', 'tipe' => 'Aset', 'saldo_normal' => 'Debit'],
            
            // Kewajiban
            ['kode_akun' => '2-1000', 'nama_akun' => 'Hutang Usaha', 'tipe' => 'Kewajiban', 'saldo_normal' => 'Kredit'],
            
            // Ekuitas
            ['kode_akun' => '3-1000', 'nama_akun' => 'Ekuitas Yayasan', 'tipe' => 'Ekuitas', 'saldo_normal' => 'Kredit'],
            
            // Pendapatan
            ['kode_akun' => '4-1000', 'nama_akun' => 'Pendapatan SPP', 'tipe' => 'Pendapatan', 'saldo_normal' => 'Kredit'],
            ['kode_akun' => '4-2000', 'nama_akun' => 'Pendapatan Daftar Ulang', 'tipe' => 'Pendapatan', 'saldo_normal' => 'Kredit'],
            ['kode_akun' => '4-3000', 'nama_akun' => 'Pendapatan Infaq', 'tipe' => 'Pendapatan', 'saldo_normal' => 'Kredit'],
            ['kode_akun' => '4-4000', 'nama_akun' => 'Pendapatan Zakat', 'tipe' => 'Pendapatan', 'saldo_normal' => 'Kredit'],
            ['kode_akun' => '4-5000', 'nama_akun' => 'Pendapatan Kencleng', 'tipe' => 'Pendapatan', 'saldo_normal' => 'Kredit'],
            ['kode_akun' => '4-6000', 'nama_akun' => 'Pendapatan Unit Usaha', 'tipe' => 'Pendapatan', 'saldo_normal' => 'Kredit'],
            
            // Beban
            ['kode_akun' => '5-1000', 'nama_akun' => 'Beban ATK', 'tipe' => 'Beban', 'saldo_normal' => 'Debit'],
            ['kode_akun' => '5-2000', 'nama_akun' => 'Beban Listrik/Air', 'tipe' => 'Beban', 'saldo_normal' => 'Debit'],
            ['kode_akun' => '5-3000', 'nama_akun' => 'Beban Seragam', 'tipe' => 'Beban', 'saldo_normal' => 'Debit'],
            ['kode_akun' => '5-4000', 'nama_akun' => 'Beban Konsumsi', 'tipe' => 'Beban', 'saldo_normal' => 'Debit'],
            ['kode_akun' => '5-5000', 'nama_akun' => 'Beban Pemeliharaan', 'tipe' => 'Beban', 'saldo_normal' => 'Debit'],
            ['kode_akun' => '5-6000', 'nama_akun' => 'Beban Transportasi', 'tipe' => 'Beban', 'saldo_normal' => 'Debit'],
            ['kode_akun' => '5-7000', 'nama_akun' => 'Beban Honor', 'tipe' => 'Beban', 'saldo_normal' => 'Debit'],
        ];

        foreach ($coaData as $coa) {
            COA::create($coa);
        }
    }
}
EOF

cat > config/app.php << 'EOF'
<?php

return [
    'name' => env('APP_NAME', 'SIMKEU_Yayasan'),
    'env' => env('APP_ENV', 'production'),
    'debug' => (bool) env('APP_DEBUG', false),
    'url' => env('APP_URL', 'http://localhost'),
    'timezone' => 'Asia/Jakarta',
    'locale' => 'id',
    'fallback_locale' => 'en',
    'faker_locale' => 'id_ID',
    'key' => env('APP_KEY'),
    'cipher' => 'AES-256-CBC',

    'providers' => [
        Illuminate\Auth\AuthServiceProvider::class,
        Illuminate\Broadcasting\BroadcastServiceProvider::class,
        Illuminate\Bus\BusServiceProvider::class,
        Illuminate\Cache\CacheServiceProvider::class,
        Illuminate\Foundation\Providers\ConsoleSupportServiceProvider::class,
        Illuminate\Cookie\CookieServiceProvider::class,
        Illuminate\Database\DatabaseServiceProvider::class,
        Illuminate\Encryption\EncryptionServiceProvider::class,
        Illuminate\Filesystem\FilesystemServiceProvider::class,
        Illuminate\Foundation\Providers\FoundationServiceProvider::class,
        Illuminate\Hashing\HashServiceProvider::class,
        Illuminate\Mail\MailServiceProvider::class,
        Illuminate\Notifications\NotificationServiceProvider::class,
        Illuminate\Pagination\PaginationServiceProvider::class,
        Illuminate\Pipeline\PipelineServiceProvider::class,
        Illuminate\Queue\QueueServiceProvider::class,
        Illuminate\Redis\RedisServiceProvider::class,
        Illuminate\Auth\Passwords\PasswordServiceProvider::class,
        Illuminate\Session\SessionServiceProvider::class,
        Illuminate\Translation\TranslationServiceProvider::class,
        Illuminate\Validation\ValidationServiceProvider::class,
        Illuminate\View\ViewServiceProvider::class,

        Intervention\Image\ImageServiceProvider::class,
        Maatwebsite\Excel\ExcelServiceProvider::class,
        Barryvdh\DomPDF\ServiceProvider::class,
    ],

    'aliases' => [
        'App' => Illuminate\Support\Facades\App::class,
        'Arr' => Illuminate\Support\Arr::class,
        'Art' => Illuminate\Support\Facades\Artisan::class,
        'Auth' => Illuminate\Support\Facades\Auth::class,
        'Blade' => Illuminate\Support\Facades\Blade::class,
        'Broadcast' => Illuminate\Support\Facades\Broadcast::class,
        'Bus' => Illuminate\Support\Facades\Bus::class,
        'Cache' => Illuminate\Support\Facades\Cache::class,
        'Config' => Illuminate\Support\Facades\Config::class,
        'Cookie' => Illuminate\Support\Facades\Cookie::class,
        'Crypt' => Illuminate\Support\Facades\Crypt::class,
        'Date' => Illuminate\Support\Facades\Date::class,
        'DB' => Illuminate\Support\Facades\DB::class,
        'Eloquent' => Illuminate\Database\Eloquent\Model::class,
        'Event' => Illuminate\Support\Facades\Event::class,
        'File' => Illuminate\Support\Facades\File::class,
        'Gate' => Illuminate\Support\Facades\Gate::class,
        'Hash' => Illuminate\Support\Facades\Hash::class,
        'Http' => Illuminate\Support\Facades\Http::class,
        'Lang' => Illuminate\Support\Facades\Lang::class,
        'Log' => Illuminate\Support\Facades\Log::class,
        'Mail' => Illuminate\Support\Facades\Mail::class,
        'Notification' => Illuminate\Support\Facades\Notification::class,
        'Password' => Illuminate\Support\Facades\Password::class,
        'Queue' => Illuminate\Support\Facades\Queue::class,
        'RateLimit' => Illuminate\Support\Facades\RateLimiter::class,
        'Redirect' => Illuminate\Support\Facades\Redirect::class,
        'Request' => Illuminate\Support\Facades\Request::class,
        'Response' => Illuminate\Support\Facades\Response::class,
        'Route' => Illuminate\Support\Facades\Route::class,
        'Schema' => Illuminate\Support\Facades\Schema::class,
        'Session' => Illuminate\Support\Facades\Session::class,
        'Storage' => Illuminate\Support\Facades\Storage::class,
        'Str' => Illuminate\Support\Str::class,
        'URL' => Illuminate\Support\Facades\URL::class,
        'Validator' => Illuminate\Support\Facades\Validator::class,
        'View' => Illuminate\Support\Facades\View::class,
        'Image' => Intervention\Image\Facades\Image::class,
        'Excel' => Maatwebsite\Excel\Facades\Excel::class,
        'PDF' => Barryvdh\DomPDF\Facade::class,
    ],
];
EOF

cat > config/database.php << 'EOF'
<?php

use Illuminate\Database\DBAL\TimestampType;
use Illuminate\Support\Str;

return [
    'default' => env('DB_CONNECTION', 'mysql'),
    'connections' => [
        'mysql' => [
            'driver' => 'mysql',
            'url' => env('DATABASE_URL'),
            'host' => env('DB_HOST', '127.0.0.1'),
            'port' => env('DB_PORT', '3306'),
            'database' => env('DB_DATABASE', 'simkeu_yayasan'),
            'username' => env('DB_USERNAME', 'root'),
            'password' => env('DB_PASSWORD', ''),
            'unix_socket' => env('DB_SOCKET', ''),
            'charset' => 'utf8mb4',
            'collation' => 'utf8mb4_unicode_ci',
            'prefix' => '',
            'prefix_indexes' => true,
            'strict' => true,
            'engine' => null,
            'options' => extension_loaded('pdo_mysql') ? array_filter([
                PDO::MYSQL_ATTR_SSL_CA => env('MYSQL_ATTR_SSL_CA'),
            ]) : [],
        ],
    ],
    'migrations' => 'migrations',
    'redis' => [
        'client' => env('REDIS_CLIENT', 'phpredis'),
        'options' => [
            'cluster' => env('REDIS_CLUSTER', 'redis'),
            'prefix' => env('REDIS_PREFIX', Str::slug(env('APP_NAME', 'laravel'), '_').'_database_'),
        ],
        'default' => [
            'url' => env('REDIS_URL'),
            'host' => env('REDIS_HOST', '127.0.0.1'),
            'password' => env('REDIS_PASSWORD', null),
            'port' => env('REDIS_PORT', '6379'),
            'database' => env('REDIS_DB', '0'),
        ],
        'cache' => [
            'url' => env('REDIS_URL'),
            'host' => env('REDIS_HOST', '127.0.0.1'),
            'password' => env('REDIS_PASSWORD', null),
            'port' => env('REDIS_PORT', '6379'),
            'database' => env('REDIS_CACHE_DB', '1'),
        ],
    ],
];
EOF

echo "Project structure built successfully."
