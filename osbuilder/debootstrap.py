import ask
import shell
import platform
import re
from collections import OrderedDict


ARCHS = OrderedDict([
    ('i386', {'alias': []}),
    ('amd64', {'alias': ['x86_64']}),
    ('armhf', {'alias': []}),
    ('arm64', {'alias': []}),
])

SUITES = OrderedDict([
    ('wheezy', {'base': 'debian'}),
    ('jessie', {'base': 'debian'}),
    ('sid', {'base': 'debian'}),
    ('precise', {'base': 'ubuntu'}),
    ('trusty', {'base': 'ubuntu'}),
    ('vivid', {'base': 'ubuntu'}),
    ('wily', {'base': 'ubuntu'}),
    ('xenial', {'base': 'ubuntu'}),
])


def crawl_sources(arch, suite):
    mirrors = [
        # Debian
        'http://ftp.pt.debian.org/debian/',

        # Ubuntu
        # 'http://archive.ubuntu.com/ubuntu',
        # 'http://mirrors.fe.up.pt/ubuntu',
        'http://pt.archive.ubuntu.com/ubuntu',

        # Ubuntu arm
        'http://ports.ubuntu.com/ubuntu-ports',

        # Ubuntu extra
        'http://archive.canonical.com/ubuntu',
        'http://extras.ubuntu.com/ubuntu',
    ]

    sources = OrderedDict()

    # Get distributions
    for mirror in mirrors:
        sources[mirror] = OrderedDict()
        content = shell.stdout('wget -qO- {}/dists'.format(mirror))
        regex = r'<a href="({}[a-zA-Z0-9-]*)/">'.format(suite)
        for distribution in re.findall(regex, content, re.M):
            sources[mirror][distribution] = []

    # Get components
    for mirror, distributions in sources.items():
        for distribution, components in distributions.items():
            content = shell.stdout('wget -qO- {}/dists/{}/Release'.format(mirror, distribution))
            regex = r'([a-zA-Z0-9-]+)/binary-{}/Release$'.format(arch)
            for component in re.findall(regex, content, re.M):
                if component not in components:
                    components.append(component)

    # Cleanup
    for mirror, distributions in dict(sources).items():
        for distribution, components in dict(distributions).items():
            if any(sub in distribution for sub in ['-proposed', '-backports']):
                del distributions[distribution]
                continue

            for component in list(components):
                if not shell.bash('wget -qO/dev/null {}/dists/{}/{}/binary-{}/Release'.format(mirror, distribution, component, arch)):
                    components.remove(component)

            if not components:
                del distributions[distribution]

        if not distributions:
            del sources[mirror]

    return sources


def primary_mirror(sources):
    for mirror in sources:
        return mirror


def apt_sources_list(sources):
    text = ''

    for mirror, distributions in sources.items():
        for distribution, components in distributions.items():
            text += 'deb {} {} {}\n'.format(mirror, distribution, ' '.join(components))

    return text


def system_arch():
    processor = platform.processor()

    for arch, info in ARCHS.items():
        if processor == arch or processor in info['alias']:
            return arch


def debootstrap(rootfs, arch=system_arch(), suite='wily', include=[]):
    sources = crawl_sources(arch, suite)
    foreign = arch != system_arch()

    cmd = 'debootstrap --arch={} --variant={} {} {} {} {} {}'.format(
        arch,
        'minbase',
        '--foreign' if foreign else '',
        '--include={}'.format(','.join(include)) if include else '',
        suite,
        rootfs,
        primary_mirror(sources)
    )

    print(cmd)
    shell.bash(cmd)
