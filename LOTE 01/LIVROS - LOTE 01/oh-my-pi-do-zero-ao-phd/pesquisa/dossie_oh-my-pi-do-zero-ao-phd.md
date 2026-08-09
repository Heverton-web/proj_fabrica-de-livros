# Dossiê de Pesquisa — Oh My Pi: Do zero ao PhD

> Tema central: o Raspberry Pi como plataforma de computação — do primeiro boot
> à pesquisa e engenharia de produção. Obra de tamanho G (5 Partes, 10 capítulos,
> ~150 páginas, 20 referências por capítulo).

## Conceitos-chave

- **Raspberry Pi**: computador single-board (SBC) de baixo custo da Raspberry Pi
  Ltd., lançado em 2012, com mais de **73 milhões de unidades vendidas** e receita
  de US$ 323,2 milhões no FY25 (Raspberry Pi, Investor Relations — investors.raspberrypi.com).
- **SoC (System-on-Chip)**: chip que integra CPU, GPU, memória e periféricos. O Pi 5
  usa o **Broadcom BCM2712** (quad-core ARM Cortex-A76 de 64 bits a 2,4 GHz, GPU
  VideoCore VII, extensões criptográficas, L2 de 512 KB/núcleo e L3 de 2 MB)
  (Raspberry Pi, página do Pi 5).
- **RP1**: chip de I/O projetado internamente pela Raspberry Pi, introduzido no Pi 5,
  que substitui pontes sul tradicionais e fornece USB de alta largura de banda,
  câmera/display e **PCIe 2.0 x1 nativo** (expansão NVMe/SSD via HATs).
- **GPIO (General-Purpose Input/Output)**: header de 40 pinos com digitais, PWM,
  I2C, SPI e UART; padrão físico/elétrico de expansão da plataforma.
- **HAT (Hardware Attached on Top)**: padrão de placas filhas com identificação via
  EEPROM (ID_SD/ID_SC); no Pi 5 ganhou suporte a M.2 NVMe via PCIe.
- **Raspberry Pi Pico / RP2040 / RP2350**: linha de microcontroladores. O Pico 2 usa
  o **RP2350** com núcleos ARM Cortex-M33 ou RISC-V Hazard3 (150 MHz), criptografia
  por hardware (SHA-256), TrustZone e **PIO (Programmable I/O)** com 12 máquinas de
  estado (protocolos customizados em hardware).
- **Raspberry Pi OS**: SO oficial baseado em **Debian 12 (Bookworm)**, disponível em
  32 bits (armhf) e 64 bits (arm64, recomendado no Pi 3/4/5) (documentação oficial).
- **Raspberry Pi Imager**: utilitário oficial para gravar imagens em cartão SD/USB
  com configuração *headless* pré-instalação (SSH, Wi-Fi, hostname, usuário).
- **Bibliotecas GPIO em Python**: `gpiozero` (oficial, alto nível, padrão), `RPi.GPIO`
  (legada, **deprecada** — sem suporte ao RP1/Pi 5), `libgpiod` (interface de kernel
  moderna), `pigpio` (C, alta precisão e controle remoto por rede).
- **Edge computing / IoT**: processamento na borda da rede; o Pi é usado como nó de
  gateway/sensor com MQTT, Node-RED e inferência local.
- **Edge AI**: o **Raspberry Pi AI Kit / AI HAT+** adiciona NPU **Hailo-8 (26 TOPS)**
  ou **Hailo-8L (13 TOPS)** via PCIe para visão computacional em tempo real; a
  **AI Camera** integra coprocessador de IA ao sensor.
- **Cluster de computação**: múltiplos Pi interligados (Turing Pi, Cluster HAT,
  k3s, Kubernetes) para simular nuvem bare-metal, aprender orquestração e rodar HPC
  de baixo consumo (caso LANL — Top500).
- **Compute Module (CM4/CM5)**: linha sem conectores de consumo, voltada a produtos
  industriais; base do padrão **Revolution Pi** (DIN rail, 24V, eMMC, Modbus TCP/RTU,
  PROFINET, EtherCAT, OPC UA, CODESYS).
- **Motivo condutor proposto**: "a bancada de trabalho (workbench)" — onde o leitor
  monta, mede, programa e escala; do primeiro parafuso ao cluster.

## Artigos Científicos e Papers

- MURSHED, M. G. S.; MURPHY, C.; HOU, D.; KHAN, N.; ANANTHANARAYANAN, G.; HUSSAIN, F. *Machine Learning at the Network Edge: A Survey*. ACM Computing Surveys, 2022. Disponível em: https://doi.org/10.1145/3469029. Acesso em: 4 ago. 2026.
- FEINGOLD, R.; YU, C. *MQTT Across a Raspberry Pi 5 IoT Network Utilizing Quantum-resistant Signature Algorithms*. arXiv preprint, 2026. Disponível em: https://arxiv.org/abs/2605.13698. Acesso em: 4 ago. 2026.
- ABRAHAMSSON, P.; HELMER, S.; PHAPHOOM, N.; NICOLODI, L.; PREDA, N.; MIORI, L.; ANGRIMAN, M.; RIKKILA, J.; WANG, X.; HAMILY, K.; BUGOLONI, S. *Affordable and Energy-Efficient Cloud Computing Clusters: The Bolzano Raspberry Pi Cloud Cluster Experiment*. IEEE International Conference on Cloud Computing (CloudCom), 2017. Disponível em: https://arxiv.org/abs/1709.06815. Acesso em: 4 ago. 2026.
- CICIRELLO, V. A. *Design, Configuration, Implementation, and Performance of a Simple 32 Core Raspberry Pi Cluster*. arXiv preprint, 2024. Disponível em: https://arxiv.org/abs/1708.05264. Acesso em: 4 ago. 2026.
- PORTILLO, N. *Design and Implementation of an IoT Cluster with Raspberry Pi Powered by Solar Energy: A Theoretical Approach*. arXiv preprint, 2025. Disponível em: https://arxiv.org/abs/2503.03618. Acesso em: 4 ago. 2026.
- GARCÍA SANTACLARA, P.; FERNÁNDEZ VILAS, A.; DÍAZ REDONDO, R. P. *Prototype of Deployment of Federated Learning with IoT Devices*. ACM International Symposium on Performance Evaluation of Wireless Ad Hoc, Sensor, and Ubiquitous Networks (PE-WASUN), 2023. Disponível em: https://arxiv.org/abs/2311.14401. Acesso em: 4 ago. 2026.
- KHATER, O. H.; ALMADANI, B.; ALIYU, F.; AL-NAHARI, E. *A Real-Time DDS-Based Chest X-Ray Decision Support System for Resource-Constrained Clinics*. arXiv preprint, 2026. Disponível em: https://arxiv.org/abs/2412.07818. Acesso em: 4 ago. 2026.
- KHATTAB, S.; MELHEM, R.; MOSSÉ, D.; CHRYSANTHIS, P. *Portable Parallel Computing with the Raspberry Pi*. In: SIGCSE '18: Proceedings of the 49th ACM Technical Symposium on Computer Science Education, 2018. Disponível em: https://dl.acm.org/doi/10.1145/3077286.3077324. Acesso em: 4 ago. 2026.
- ARIZA, J. A.; GUTIERREZ, J.; TORAL, S. *Understanding the Role of Single-Board Computers in Engineering and Computer Science Education: A Systematic Literature Review*. Heliyon, v. 8, 2022. Disponível em: https://arxiv.org/abs/2203.16604. Acesso em: 4 ago. 2026.
- RASPBERRY PI COMPUTING EDUCATION RESEARCH CENTRE. *Mapping Data Literacy Trajectories in K-12 Education*. arXiv preprint, 2026. Disponível em: https://arxiv.org/abs/2603.28317. Acesso em: 4 ago. 2026.
- JOICE, A. et al. *Applications of Raspberry Pi for Precision Agriculture — A Systematic Review*. Agriculture (MDPI), v. 15, n. 3, 2025. Disponível em: https://www.mdpi.com/2077-0472/15/3/227. Acesso em: 4 ago. 2026.
- SEGERS, L. et al. *Trustworthy Environmental Monitoring Using Hardware-Accelerated IoT Nodes*. Sensors (MDPI), v. 24, n. 14, 2024. Disponível em: https://www.mdpi.com/1424-8220/24/14/4720. Acesso em: 4 ago. 2026.

## Estado da arte / ferramentas de referência

- **Raspberry Pi 5**: BCM2712 (Cortex-A76 2,4 GHz), 1–16 GB LPDDR4X-4267, GPU
  VideoCore VII (OpenGL ES 3.1, Vulkan 1.3), chip de I/O RP1, PCIe 2.0 x1,
  fonte 5V/5A (27W) USB-C, refrigeração ativa recomendada. Produção garantida até
  **janeiro de 2036** (raspberrypi.com/products/raspberry-pi-5).
- **Benchmarks do Pi 5 vs Pi 4**: Geekbench 6 ≈ 764 single-core / 1604 multi-core
  (2,2–2,4× o Pi 4); criptografia até 45× mais rápida; RAMspeed 4–6× na banda de
  memória (raspberrypi.com/news/benchmarking-raspberry-pi-5).
- **Raspberry Pi Zero 2 W**: SiP RP3A0 (Cortex-A53 quad-core 1 GHz), 512 MB,
  Wi-Fi b/g/n + BT 4.2, 65×30 mm; ~5× mais rápido que o Zero original; produção até
  **janeiro de 2030** (raspberrypi.com/products/raspberry-pi-zero-2-w).
- **Raspberry Pi Pico 2 / RP2350**: dual ARM Cortex-M33 ou dual RISC-V Hazard3 a
  150 MHz, SHA-256 em hardware, TrustZone, PIO com 12 máquinas de estado; versão
  Pico 2 W com Wi-Fi 802.11n e BT 5.2; produção até **janeiro de 2040**.
- **Raspberry Pi OS Bookworm**: base Debian 12; 64 bits recomendado (arm64);
  instalação via Imager com preconfiguração headless (SSH, Wi-Fi, hostname);
  ferramentas `raspi-config`, `rpi-eeprom-update`, systemd
  (raspberrypi.com/documentation/computers/os.html).
- **Bibliotecas GPIO**: `gpiozero` oficial (padrão, alto nível, pin factories
  `lgpio`/`RPi.GPIO`), `RPi.GPIO` deprecada (sem suporte RP1/Pi 5), `libgpiod`
  (kernel nativo), `pigpio` (C, precisão, controle remoto)
  (github.com/gpiozero/gpiozero; github.com/joan2937/pigpio).
- **Docker no Pi**: suporte oficial ARM64 via Docker Engine (docker-ce); contêineres
  nativos para arquitetura ARM.
- **Kubernetes leve**: **k3s** (Rancher, binário único <70 MB, suporte ARM64) e
  **MicroK8s** (Canonical, snap; requer `cgroup_enable=memory cgroup_memory=1` em
  `/boot/firmware/cmdline.txt`).
- **Edge AI**: AI Kit / AI HAT+ com **Hailo-8 (26 TOPS)** ou **Hailo-8L (13 TOPS)**
  via PCIe; AI Camera com coprocessador de IA no sensor; detecção/segmentação/
  rastreamento em tempo real na borda (raspberrypi.com/documentation/accessories/ai-kit.html).
- **Indústria**: Compute Module 4/5; padrão **Revolution Pi** (DIN rail, 24V
  protegida, eMMC soldada, Modbus TCP/RTU, PROFINET, EtherCAT, OPC UA); soft-PLC
  **CODESYS** (IEC 61131-3) (revolutionpi.com/en/raspberry-pi-vs-industrial-raspberry-pi).
- **Clusters**: Turing Pi, Cluster HAT, HPC de baixo consumo; caso LANL com centenas
  de nós para testar resiliência de software de supercomputação
  (turingpi.com/12-amazing-raspberry-pi-cluster-use-cases; top500.org).

## Casos de uso corporativos

- **Inspeção industrial e visão na borda**: qualidade em linhas de montagem,
  contagem de fluxo, vigilância orientada por privacidade, controle de processos
  com AI Kit + câmera (documentação oficial AI Kit).
- **Automação e Indústria 4.0**: PLCs baseados em Compute Module com CODESYS;
  barramentos industriais (Modbus, PROFINET, EtherCAT, OPC UA) via Revolution Pi.
- **Cluster/supercomputação de teste**: LANL usou centenas de Raspberry Pi para
  avaliar resiliência e tolerância a falhas em HPC distribuído (Top500).
- **Testbeds de nuvem/DevOps**: clusters Pi (Turing Pi, Cluster HAT) para simular
  nuvem bare-metal, aprender Kubernetes/Docker, CI/CD de baixo custo.
- **Monitoramento ambiental e biologia de campo**: British Ecological Society relata
  uso massivo de Pi + painel solar para monitoramento remoto de microclimas,
  contagem automática de aves, fenologia de plantas.
- **Agricultura de precisão**: coleta de sensores de solo/umidade, câmeras
  multiespectrais, otimização de irrigação e detecção precoce de doenças
  (Joice et al., MDPI 2025).
- **Saúde de baixo custo**: sistema de decisão para raios-X de tórax em clínicas
  com poucos recursos usando DDS + Pi (Khater et al., arXiv 2026).
- **Áudio e instrumentação científica**: Neurorack/Eurorack e síntese com redes
  neurais em tempo real no IRCAM.
- **Educação STEM**: ensino de computação paralela portátil com Pi (Khattab et al.,
  SIGCSE 2018); revisão sistemática sobre SBCs no ensino de engenharia e ciência da
  computação (Ariza et al., Heliyon 2022).

## Limitações e controvérsias

- **Cartão microSD**: baixa resistência a ciclos de escrita (*write endurance*) e
  corrupção sob queda de energia; produção exige SSD NVMe via PCIe ou eMMC onboard.
- **Cadeia de suprimentos**: escassez global de semicondutores restringiu
  severamente a oferta; preços inflacionados por revenda; incerteza de *lifecycle*
  afeta adoção industrial (mender.io/blog/raspberry-pi-in-production).
- **Segurança de IoT**: configurações padrão flexíveis geram risco de "Rogue
  Raspberry Pi" em redes corporativas; regulamentações como o EU Cyber Resilience
  Act exigem *hardening* (secure boot, chaves, OTA seguro).
- **Conformidade industrial**: placas de consumo falham em EMC e vibração; exigem
  encapsulamento (Revolution Pi) e graus de proteção para ambientes fabris.
- **Transição 64-bit**: bibliotecas legadas de hardware, drivers de terceiros e
  RPi.GPIO enfrentaram atritos na migração para arm64/Pi 5 (RP1).
- **Suporte de software**: RPi.GPIO deprecada; algumas ferramentas exigem adaptação
  (pigpio) para novos chips — documentação e ecossistema mitigam, mas há custo de
  portabilidade.
- **Aprendizado de máquina na borda**: modelos limitados por RAM/CPU sem NPU;
  Hailo resolve inferência, mas exige pipeline de conversão de modelos (HDF/ONNX).

## Fontes brutas (para Nó 7 — Auditor de Rastreabilidade)

- RASPBERRY PI. *Raspberry Pi 5*. Disponível em: https://www.raspberrypi.com/products/raspberry-pi-5/. Acesso em: 4 ago. 2026.
- RASPBERRY PI. *Raspberry Pi Pico 2*. Disponível em: https://www.raspberrypi.com/products/raspberry-pi-pico-2/. Acesso em: 4 ago. 2026.
- RASPBERRY PI. *Raspberry Pi Zero 2 W*. Disponível em: https://www.raspberrypi.com/products/raspberry-pi-zero-2-w/. Acesso em: 4 ago. 2026.
- RASPBERRY PI. *Benchmarking Raspberry Pi 5*. Disponível em: https://www.raspberrypi.com/news/benchmarking-raspberry-pi-5/. Acesso em: 4 ago. 2026.
- RASPBERRY PI. *Investor Relations*. Disponível em: https://investors.raspberrypi.com/. Acesso em: 4 ago. 2026.
- RASPBERRY PI. *Documentation — Operating Systems*. Disponível em: https://www.raspberrypi.com/documentation/computers/os.html. Acesso em: 4 ago. 2026.
- RASPBERRY PI. *Documentation — AI Kit*. Disponível em: https://www.raspberrypi.com/documentation/accessories/ai-kit.html. Acesso em: 4 ago. 2026.
- MURSHED, M. G. S.; MURPHY, C.; HOU, D.; KHAN, N.; ANANTHANARAYANAN, G.; HUSSAIN, F. *Machine Learning at the Network Edge: A Survey*. ACM Computing Surveys, 2022. Disponível em: https://doi.org/10.1145/3469029. Acesso em: 4 ago. 2026.
- FEINGOLD, R.; YU, C. *MQTT Across a Raspberry Pi 5 IoT Network Utilizing Quantum-resistant Signature Algorithms*. arXiv, 2026. Disponível em: https://arxiv.org/abs/2605.13698. Acesso em: 4 ago. 2026.
- ABRAHAMSSON, P.; HELMER, S.; PHAPHOOM, N.; NICOLODI, L.; PREDA, N.; MIORI, L.; ANGRIMAN, M.; RIKKILA, J.; WANG, X.; HAMILY, K.; BUGOLONI, S. *Affordable and Energy-Efficient Cloud Computing Clusters: The Bolzano Raspberry Pi Cloud Cluster Experiment*. IEEE CloudCom, 2017. Disponível em: https://arxiv.org/abs/1709.06815. Acesso em: 4 ago. 2026.
- CICIRELLO, V. A. *Design, Configuration, Implementation, and Performance of a Simple 32 Core Raspberry Pi Cluster*. arXiv, 2024. Disponível em: https://arxiv.org/abs/1708.05264. Acesso em: 4 ago. 2026.
- PORTILLO, N. *Design and Implementation of an IoT Cluster with Raspberry Pi Powered by Solar Energy: A Theoretical Approach*. arXiv, 2025. Disponível em: https://arxiv.org/abs/2503.03618. Acesso em: 4 ago. 2026.
- GARCÍA SANTACLARA, P.; FERNÁNDEZ VILAS, A.; DÍAZ REDONDO, R. P. *Prototype of Deployment of Federated Learning with IoT Devices*. ACM PE-WASUN, 2023. Disponível em: https://arxiv.org/abs/2311.14401. Acesso em: 4 ago. 2026.
- KHATER, O. H.; ALMADANI, B.; ALIYU, F.; AL-NAHARI, E. *A Real-Time DDS-Based Chest X-Ray Decision Support System for Resource-Constrained Clinics*. arXiv, 2026. Disponível em: https://arxiv.org/abs/2412.07818. Acesso em: 4 ago. 2026.
- KHATTAB, S.; MELHEM, R.; MOSSÉ, D.; CHRYSANTHIS, P. *Portable Parallel Computing with the Raspberry Pi*. In: SIGCSE '18: Proceedings of the 49th ACM Technical Symposium on Computer Science Education, 2018. Disponível em: https://dl.acm.org/doi/10.1145/3077286.3077324. Acesso em: 4 ago. 2026.
- ARIZA, J. A.; GUTIERREZ, J.; TORAL, S. *Understanding the Role of Single-Board Computers in Engineering and Computer Science Education: A Systematic Literature Review*. Heliyon, v. 8, 2022. Disponível em: https://arxiv.org/abs/2203.16604. Acesso em: 4 ago. 2026.
- RASPBERRY PI COMPUTING EDUCATION RESEARCH CENTRE. *Mapping Data Literacy Trajectories in K-12 Education*. arXiv, 2026. Disponível em: https://arxiv.org/abs/2603.28317. Acesso em: 4 ago. 2026.
- JOICE, A. et al. *Applications of Raspberry Pi for Precision Agriculture — A Systematic Review*. Agriculture (MDPI), v. 15, n. 3, 2025. Disponível em: https://www.mdpi.com/2077-0472/15/3/227. Acesso em: 4 ago. 2026.
- SEGERS, L. et al. *Trustworthy Environmental Monitoring Using Hardware-Accelerated IoT Nodes*. Sensors (MDPI), v. 24, n. 14, 2024. Disponível em: https://www.mdpi.com/1424-8220/24/14/4720. Acesso em: 4 ago. 2026.
- REVOLUTION PI. *Raspberry Pi vs. Industrial Raspberry Pi*. Disponível em: https://revolutionpi.com/en/raspberry-pi-vs-industrial-raspberry-pi. Acesso em: 4 ago. 2026.
- MENDER. *Raspberry Pi in Production: Considerations*. Disponível em: https://mender.io/blog/raspberry-pi-in-production. Acesso em: 4 ago. 2026.
- TURING PI. *12 Amazing Raspberry Pi Cluster Use Cases*. Disponível em: https://turingpi.com/12-amazing-raspberry-pi-cluster-use-cases/. Acesso em: 4 ago. 2026.
- TOP500. *LANL Turns to Raspberry Pi for Supercomputing Solution*. Disponível em: https://www.top500.org/news/lanl-turns-to-raspberry-pi-for-supercomputing-solution/. Acesso em: 4 ago. 2026.
- GITHUB. *gpiozero*. Disponível em: https://github.com/gpiozero/gpiozero. Acesso em: 4 ago. 2026.
- GITHUB. *pigpio*. Disponível em: https://github.com/joan2937/pigpio. Acesso em: 4 ago. 2026.
- GITHUB. *Raspberry Pi Imager*. Disponível em: https://github.com/raspberrypi/rpi-imager. Acesso em: 4 ago. 2026.
