include supervisor

Exec {
  path => '/usr/bin:/usr/sbin:/bin:/usr/local/bin',
}

group { 'regcert':
  ensure => 'present',
}

user { 'regcert':
  ensure => 'present',
  system => true,
  gid => 'regcert',
  require => Group['regcert']
}

exec { 'apt-get update':
  command => '/usr/bin/apt-get update',
}

$package_deps = [
  'git', 'supervisor', 'npm', 'gettext',

  'libpq-dev',
]

package { $package_deps: 
  require => Exec['apt-get update'],
}

$regcert_dir = '/srv/regcert'
$regcert_data_dir = '/srv/regcert_data'

vcsrepo { $regcert_dir:
  ensure   => latest,
  provider => git,
  source   => 'https://github.com/interlegis/regcert',
  require  => Package['git'],
}

# Bower ######################################################################


package { 'bower':
  name            => 'bower',
  provider        => 'npm',
  install_options => ['-g'],
  require         => Package['npm'],
}

file { '/usr/bin/node':
  ensure  => 'link',
  target  => '/usr/bin/nodejs',
  require => Package['bower'],
}

exec { 'bower dependencies':
  command => 'bower install --allow-root',
  cwd     => $regcert_dir,
  require => [
    Package['bower'],
    Vcsrepo[$regcert_dir],
    file['/usr/bin/node'],
  ],
}


# Python #####################################################################

if !defined(Class['python']) {
  class { 'python':
    version    => 'system',
    dev        => true,
    virtualenv => true,
    pip        => true,
  }
}

$regcert_venv_dir = '/srv/.virtualenvs/regcert'

file { ['/srv/.virtualenvs',]:
  ensure => 'directory',
}

python::virtualenv { $regcert_venv_dir:
  require => File['/srv/.virtualenvs'],
}

python::requirements { "${regcert_dir}/requirements/prod-requirements.txt":
  virtualenv => $regcert_venv_dir,
  forceupdate => true,
  require     => [
    Python::Virtualenv[$regcert_venv_dir],
    Vcsrepo[$regcert_dir],
    Package[$package_deps],
  ],
}


# Supervisor #################################################################

supervisor::app { 'regcert':
  command   => "${regcert_dir}/bin/run_regcert",
  directory => $regcert_dir,
  require   => Vcsrepo[$regcert_dir],
}


# NGINX ######################################################################

file { [
  '/var/log/regcert',
  '/var/run/regcert',
]:
  ensure => 'directory',
  owner => 'regcert',
  group => 'regcert',
  require => Vcsrepo[$regcert_dir],
}

class { 'nginx': }

nginx::resource::upstream { 'regcert_app_server':
  members               => ['127.0.0.1:8001'],
  upstream_fail_timeout => 0,
}

$regcert_vhost = 'localhost'

nginx::resource::vhost { $regcert_vhost:
  client_max_body_size => '4G',
  access_log           => '/var/log/regcert/regcert-access.log',
  error_log            => '/var/log/regcert/regcert-error.log',
  use_default_location => false,
  require              => Vcsrepo[$regcert_dir],
  # TODO tentar usar try_files ao inves desse "if"
  #   vide http://stackoverflow.com/questions/19845566/in-nginxs-configuration-could-if-f-request-filename-cause-a-performan
  # XXX este raw_append foi uma apelacao devido a limitacoes do modulo nginx
  raw_append           => '
  location / {
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header Host $http_host;
    proxy_redirect off;
    if (!-f $request_filename) {
      proxy_pass http://regcert_app_server;
      break;
    }
  }
  '
}

nginx::resource::location { '/static/':
  vhost          => $regcert_vhost,
  location_alias => '/srv/regcert/src/static_root/',
}

