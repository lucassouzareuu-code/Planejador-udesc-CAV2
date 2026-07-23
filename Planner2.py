import tkinter as tk
from tkinter import ttk, messagebox
from typing import List, Dict, Optional

# --- Configurações & Constantes ---
DAYS = ["SEGUNDA", "TERÇA", "QUARTA", "QUINTA", "SEXTA", "SÁBADO"]
START_HOUR = 7
START_MINUTE = 30
SLOT_DURATION_MIN = 50
TOTAL_SLOTS = 16


def get_slot_time_str(slot_idx: int) -> str:
    """Retorna a representação textual do slot de horário."""
    times = [
        "08:00 - 08:50", "08:50 - 09:40", "09:50 - 10:40", "10:40 - 11:30", "11:30 - 12:20",
        "13:10 - 14:00", "14:00 - 14:50", "14:50 - 15:40", "16:00 - 16:50", "16:50 - 17:40",
        "17:40 - 18:30", "18:30 - 19:20", "19:20 - 20:10", "20:10 - 21:00", "21:00 - 21:50", "21:50 - 22:40"
    ]
    if slot_idx < len(times):
        return times[slot_idx]
    return f"Slot {slot_idx}"


# --- Modelos de Dados ---
class Course:
    def __init__(self, code: str, name: str, credits: int, schedule: Dict[str, List[int]]):
        self.code = code
        self.name = name
        self.credits = credits
        self.schedule = schedule

    def __str__(self):
        return f"[{self.code}] {self.name} ({self.credits}h)"


class CoursePlannerApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title(
            "UDESC CAV - Planejador de Matrícula Medicina Veterinária")
        self.root.geometry("1200x800")

        # 1. Inicialização do estado / variáveis de dados
        self.available_courses: List[Course] = []
        self.registered_courses: List[Course] = []
        self.filtered_courses: List[Course] = []

        # Variáveis Tkinter
        self.search_var = tk.StringVar()
        self.registered_count_var = tk.StringVar(
            value="Disciplinas Selecionadas (0):")

        # Popula catálogo
        self._populate_initial_catalog()

        # 2. Construção da Interface (UI)
        self._build_menu()
        self._build_layout()

        # 3. Atualizações e renderizações iniciais
        self.update_course_list()
        self.draw_schedule_grid()
        self.update_registered_count()

    def _populate_initial_catalog(self):
        """Catálogo completo de Medicina Veterinária UDESC CAV."""
        self.available_courses = [
            # 1ª FASE
            Course("ANAT1-TEO", "Anatomia I (Teórica)", 72,
                   {"SEGUNDA": [0, 1], "TERÇA": [0, 1]}),
            Course("ANAT1-A", "Anatomia I (Turma A)", 36, {"QUINTA": [10]}),
            Course("ANAT1-B", "Anatomia I (Turma B)", 36, {"QUARTA": [0, 1]}),
            Course("ANAT1-C", "Anatomia I (Turma C)", 36, {"SEXTA": [0, 1]}),
            Course("ANAT1-D", "Anatomia I (Turma D)", 36, {"SEXTA": [2, 10]}),
            Course("HIST1-TEO", "Histologia Geral (Teórica)",
                   72, {"SEGUNDA": [2, 3]}),
            Course("HIST1-A", "Histologia Geral (Turma A)",
                   36, {"QUARTA": [0, 1]}),
            Course("HIST1-B", "Histologia Geral (Turma B)",
                   36, {"QUINTA": [6, 7]}),
            Course("HIST1-C", "Histologia Geral (Turma C)",
                   36, {"QUARTA": [6, 7]}),
            Course("HIST1-D", "Histologia Geral (Turma D)",
                   36, {"QUARTA": [8, 9]}),
            Course("SOCIO-1", "Sociologia Aplicada", 36, {"SEGUNDA": [2, 3]}),
            Course("ECOL-1", "Ecologia e Desenvolvimento",
                   36, {"TERÇA": [2, 3]}),
            Course("BIOQ1-A", "Bioquímica de Biomoléculas (Turma A)",
                   54, {"TERÇA": [6, 7], "QUARTA": [6, 7]}),
            Course("BIOQ1-B", "Bioquímica de Biomoléculas (Turma B)",
                   54, {"QUARTA": [8, 9]}),
            Course("BIOQ1-C", "Bioquímica de Biomoléculas (Turma C)",
                   54, {"QUINTA": [6, 7]}),
            Course("ESTAT-1", "Estatística e Experimentação",
                   54, {"SEGUNDA": [6, 7, 8]}),
            Course("EXTEN-1", "Extensão, Comunicação e Sociedade",
                   36, {"SEXTA": [6, 7]}),
            Course("COMPOR-1", "Comportamento e Bem-Estar Animal",
                   36, {"QUINTA": [8, 9]}),

            # 2ª FASE
            Course("ANAT2-TEO", "Anatomia II (Teórica)", 72,
                   {"SEGUNDA": [0, 1], "TERÇA": [2, 3]}),
            Course("ANAT2-A", "Anatomia II (Turma A)",
                   36, {"QUINTA": [6, 7], "SEXTA": [8]}),
            Course("ANAT2-B", "Anatomia II (Turma B)", 36,
                   {"QUINTA": [8], "SÁBADO": [9, 10]}),
            Course("ANAT2-C", "Anatomia II (Turma C)", 36,
                   {"QUINTA": [10, 11], "SEXTA": [11]}),
            Course("ANAT2-D", "Anatomia II (Turma D)", 36,
                   {"SÁBADO": [0, 1], "SEXTA": [10, 11]}),
            Course("PARAS1-TEO", "Parasitologia I (Teórica)",
                   72, {"SEGUNDA": [2, 3]}),
            Course("PARAS1-A", "Parasitologia I (Turma A)",
                   36, {"SEGUNDA": [0, 1]}),
            Course("PARAS1-B", "Parasitologia I (Turma B)",
                   36, {"QUINTA": [11]}),
            Course("PARAS1-C", "Parasitologia I (Turma C)",
                   36, {"QUINTA": [2, 3]}),
            Course("PARAS1-D", "Parasitologia I (Turma D)",
                   36, {"SEXTA": [6, 7]}),
            Course("HIST2-TEO", "Histologia e Embriologia Vet. (Teórica)",
                   72, {"SEGUNDA": [2, 3], "QUINTA": [0]}),
            Course("HIST2-A", "Histologia e Embriologia (Turma A)",
                   36, {"SEGUNDA": [6, 7]}),
            Course("HIST2-B", "Histologia e Embriologia (Turma B)",
                   36, {"SEGUNDA": [8, 9]}),
            Course("HIST2-C", "Histologia e Embriologia (Turma C)",
                   36, {"TERÇA": [6, 7]}),
            Course("HIST2-D", "Histologia e Embriologia (Turma D)",
                   36, {"SEXTA": [6, 7]}),
            Course("GENET-TEO", "Genética (Teórica)", 54, {"SEXTA": [0, 1]}),
            Course("GENET-A", "Genética (Turma A)", 36, {"SEXTA": [2, 3]}),
            Course("GENET-B", "Genética (Turma B)", 36, {"SEXTA": [6, 7]}),
            Course("BIOQM-TEO", "Bioquímica Metabólica (Teórica)",
                   54, {"SEXTA": [2, 3]}),
            Course("BIOQM-A", "Bioquímica Metabólica (Turma A)",
                   36, {"SEGUNDA": [6, 7]}),
            Course("BIOQM-B", "Bioquímica Metabólica (Turma B)",
                   36, {"TERÇA": [6, 7, 8]}),
            Course("FISIO1-TEO", "Fisiologia I (Teórica)",
                   72, {"QUINTA": [5, 6, 7]}),
            Course("FISIO1-A", "Fisiologia I (Turma A)",
                   36, {"SEGUNDA": [8, 9]}),
            Course("FISIO1-B", "Fisiologia I (Turma B)",
                   36, {"SEGUNDA": [10, 11]}),
            Course("FISIO1-C", "Fisiologia I (Turma C)",
                   36, {"QUINTA": [10, 11]}),
            Course("FISIO1-D", "Fisiologia I (Turma D)",
                   36, {"TERÇA": [10, 11]}),

            # 3ª FASE
            Course("IMUNO-TEO", "Imunologia (Teórica)",
                   54, {"SEGUNDA": [0, 1]}),
            Course("IMUNO-A", "Imunologia (Turma A)", 36, {"SEGUNDA": [11]}),
            Course("IMUNO-B", "Imunologia (Turma B)", 36, {"SEGUNDA": [10]}),
            Course("MICRO-TEO", "Microbiologia Geral (Teórica)",
                   72, {"SEGUNDA": [2, 3]}),
            Course("MICRO-A", "Microbiologia Geral (Turma A)",
                   36, {"SEGUNDA": [8, 9]}),
            Course("MICRO-B", "Microbiologia Geral (Turma B)",
                   36, {"TERÇA": [6, 7]}),
            Course("MICRO-C", "Microbiologia Geral (Turma C)",
                   36, {"TERÇA": [8, 9]}),
            Course("MICRO-D", "Microbiologia Geral (Turma D)",
                   36, {"SEGUNDA": [6, 7]}),
            Course("ANATT-TEO", "Anatomia Topográfica (Teórica)",
                   54, {"QUARTA": [6, 7]}),
            Course("ANATT-A", "Anatomia Topográfica (Turma A)",
                   36, {"QUINTA": [2, 3]}),
            Course("ANATT-B", "Anatomia Topográfica (Turma B)",
                   36, {"QUINTA": [6, 7]}),
            Course("ANATT-C", "Anatomia Topográfica (Turma C)",
                   36, {"SEXTA": [8, 9]}),
            Course("ANATT-D", "Anatomia Topográfica (Turma D)",
                   36, {"SEXTA": [6, 7]}),

            # 4ª FASE
            Course("NUTRI-4", "Nutrição Animal", 54,
                   {"QUARTA": [0, 1], "QUINTA": [0]}),
            Course("EPIDE-4", "Epidemiologia", 36, {"QUINTA": [2, 3]}),
            Course("ECONO-4", "Economia e Administração",
                   54, {"SEXTA": [0, 1], "QUINTA": [6, 7]}),
            Course("MELHO-4", "Melhoramento Animal", 36, {"QUINTA": [8, 9]}),
            Course("FISIO2-TEO", "Fisiologia II (Teórica)",
                   72, {"SEGUNDA": [0, 1]}),
            Course("FISIO2-A", "Fisiologia II (Turma A)",
                   36, {"SEGUNDA": [2, 3]}),
            Course("FISIO2-B", "Fisiologia II (Turma B)",
                   36, {"TERÇA": [0, 1]}),
            Course("FISIO2-C", "Fisiologia II (Turma C)",
                   36, {"TERÇA": [6, 7]}),
            Course("FISIO2-D", "Fisiologia II (Turma D)",
                   36, {"QUARTA": [8, 9]}),
            Course("FARM1-TEO", "Farmacologia Geral (Teórica)",
                   72, {"SEGUNDA": [6, 7]}),
            Course("FARM1-A", "Farmacologia Geral (Turma A)",
                   36, {"TERÇA": [8, 9]}),
            Course("FARM1-B", "Farmacologia Geral (Turma B)",
                   36, {"QUARTA": [2, 3]}),
            Course("FARM1-C", "Farmacologia Geral (Turma C)",
                   36, {"TERÇA": [2, 3]}),
            Course("MICRE-TEO", "Microbiologia Especial (Teórica)",
                   72, {"QUARTA": [2, 3], "SEXTA": [2, 3, 4]}),
            Course("MICRE-B", "Microbiologia Especial (Turma B)",
                   36, {"QUARTA": [6, 7]}),
            Course("MICRE-C", "Microbiologia Especial (Turma C)",
                   36, {"QUARTA": [8, 9]}),

            # 5ª FASE
            Course("FORRA-5", "Forragicultura", 54, {"SEXTA": [0, 1, 2]}),
            Course("SEMIO-TEO", "Semiologia (Teórica)",
                   90, {"SEGUNDA": [1, 2, 3]}),
            Course("SEMIO-A", "Semiologia (Turma A)", 36, {"TERÇA": [2, 3]}),
            Course("SEMIO-B", "Semiologia (Turma B)", 36, {"QUARTA": [2, 3]}),
            Course("SEMIO-C", "Semiologia (Turma C)", 36, {"QUINTA": [2, 3]}),
            Course("SEMIO-D", "Semiologia (Turma D)", 36, {"SEXTA": [2, 3]}),
            Course("FARMD-TEO", "Farmacodinâmica (Teórica)",
                   72, {"TERÇA": [0, 1]}),
            Course("FARMD-A", "Farmacodinâmica (Turma A)",
                   36, {"QUINTA": [0, 1]}),
            Course("FARMD-B", "Farmacodinâmica (Turma B)",
                   36, {"QUINTA": [2, 3]}),
            Course("FARMD-C", "Farmacodinâmica (Turma C)",
                   36, {"SEXTA": [6, 7]}),
            Course("PATCL-TEO", "Patologia Clínica Vet. (Teórica)",
                   72, {"TERÇA": [6, 7]}),
            Course("PATCL-A", "Patologia Clínica Vet. (Turma A)",
                   36, {"QUARTA": [0, 1]}),
            Course("PATCL-B", "Patologia Clínica Vet. (Turma B)",
                   36, {"QUARTA": [2, 3]}),
            Course("PATCL-C", "Patologia Clínica Vet. (Turma C)",
                   36, {"QUARTA": [6, 7]}),
            Course("PATCL-D", "Patologia Clínica Vet. (Turma D)",
                   36, {"QUINTA": [0, 1]}),
            Course("PATG-TEO", "Patologia Geral (Teórica)",
                   90, {"SEGUNDA": [6, 7, 8]}),
            Course("PATG-A", "Patologia Geral (Turma A)",
                   36, {"TERÇA": [2, 3]}),
            Course("PATG-B", "Patologia Geral (Turma B)",
                   36, {"TERÇA": [8, 9]}),
            Course("PATG-C", "Patologia Geral (Turma C)",
                   36, {"QUARTA": [8, 9]}),
            Course("ALIMA-5", "Alimentos e Alimentação Animal",
                   90, {"QUINTA": [6, 7, 8, 9, 10]}),
            Course("COEXT-5", "Comunicação e Extensão Rural",
                   36, {"SEGUNDA": [9, 10]}),

            # 6ª FASE
            Course("SUINO-TEO", "Suinocultura (Teórica)",
                   54, {"SEGUNDA": [0, 1]}),
            Course("SUINO-A", "Suinocultura (Turma A)", 36, {"SEGUNDA": [6]}),
            Course("SUINO-B", "Suinocultura (Turma B)", 36, {"SEGUNDA": [7]}),
            Course("SUINO-C", "Suinocultura (Turma C)", 36, {"SEGUNDA": [8]}),
            Course("INFEC-TEO", "Doenças Infectocontagiosas (Teórica)",
                   72, {"TERÇA": [0, 1, 2]}),
            Course("INFEC-A", "Doenças Infectocontagiosas (Turma A)",
                   36, {"QUINTA": [6, 7]}),
            Course("INFEC-B", "Doenças Infectocontagiosas (Turma B)",
                   36, {"SEXTA": [8, 9]}),
            Course("INFEC-C", "Doenças Infectocontagiosas (Turma C)",
                   36, {"QUARTA": [8, 9]}),
            Course("PARAS2-TEO", "Doenças Parasitárias (Teórica)",
                   72, {"QUARTA": [0, 1]}),
            Course("PARAS2-A", "Doenças Parasitárias (Turma A)",
                   36, {"TERÇA": [6, 7]}),
            Course("PARAS2-B", "Doenças Parasitárias (Turma B)",
                   36, {"TERÇA": [9, 10, 11]}),
            Course("PARAS2-D", "Doenças Parasitárias (Turma D)",
                   36, {"QUARTA": [6, 7]}),
            Course("PARAS2-E", "Doenças Parasitárias (Turma E)",
                   36, {"TERÇA": [8]}),
            Course("CLINR-TEO", "Clínica Médica de Ruminantes (Teórica)",
                   72, {"QUINTA": [0, 1, 2]}),
            Course("CLINR-A", "Clínica Médica de Ruminantes (Turma A)",
                   36, {"SEGUNDA": [6, 7]}),
            Course("CLINR-B", "Clínica Médica de Ruminantes (Turma B)",
                   36, {"TERÇA": [8, 9]}),
            Course("CLINR-C", "Clínica Médica de Ruminantes (Turma C)",
                   36, {"QUARTA": [8, 9]}),
            Course("CLINR-D", "Clínica Médica de Ruminantes (Turma D)",
                   36, {"QUINTA": [6, 7]}),
            Course("PATESP-TEO", "Patologia Especial (Teórica)",
                   72, {"SEXTA": [0, 1, 2]}),
            Course("PATESP-A", "Patologia Especial (Turma A)",
                   36, {"SEXTA": [6, 7]}),
            Course("PATESP-B", "Patologia Especial (Turma B)",
                   36, {"SEXTA": [8, 9]}),
            Course("PATESP-C", "Patologia Especial (Turma C)",
                   36, {"SEXTA": [8, 9]}),
            Course("PISCI-7", "Piscicultura", 36, {"QUARTA": [2, 3, 4]}),
            Course("TERAP-7", "Terapêutica Veterinária",
                   36, {"SEGUNDA": [2, 3]}),

            # 7ª FASE
            Course("ANEST-TEO", "Anestesiologia (Teórica)",
                   54, {"SEGUNDA": [1, 2]}),
            Course("ANEST-A", "Anestesiologia (Turma A)",
                   36, {"SEGUNDA": [6, 7]}),
            Course("ANEST-B", "Anestesiologia (Turma B)",
                   36, {"TERÇA": [6, 7]}),
            Course("ANEST-C", "Anestesiologia (Turma C)",
                   36, {"TERÇA": [8, 9]}),
            Course("ANEST-D", "Anestesiologia (Turma D)",
                   36, {"TERÇA": [1, 2]}),
            Course("TCIR-TEO", "Técnica Cirúrgica (Teórica)",
                   72, {"SEGUNDA": [8, 9]}),
            Course("TCIR-A", "Técnica Cirúrgica (Turma A)",
                   36, {"TERÇA": [0, 1, 2]}),
            Course("TCIR-B", "Técnica Cirúrgica (Turma B)",
                   36, {"TERÇA": [6, 7, 8]}),
            Course("TCIR-C", "Técnica Cirúrgica (Turma C)",
                   36, {"QUARTA": [0, 1, 2]}),
            Course("TCIR-D", "Técnica Cirúrgica (Turma D)",
                   36, {"QUARTA": [6, 7, 8]}),
            Course("DIAG-TEO", "Diagnóstico por Imagem (Teórica)",
                   54, {"SEGUNDA": [10]}),
            Course("DIAG-A", "Diagnóstico por Imagem (Turma A)",
                   36, {"QUARTA": [1, 2]}),
            Course("DIAG-B", "Diagnóstico por Imagem (Turma B)",
                   36, {"QUARTA": [6, 7]}),
            Course("DIAG-C", "Diagnóstico por Imagem (Turma C)",
                   36, {"QUARTA": [8, 9]}),
            Course("DIAG-D", "Diagnóstico por Imagem (Turma D)",
                   36, {"QUINTA": [8, 9]}),
            Course("CLINC-TEO", "Clínica Médica de Cães e Gatos (Teórica)",
                   72, {"QUINTA": [0, 1, 2]}),
            Course("CLINC-A", "Clínica Médica de Cães e Gatos (Turma A)",
                   36, {"SEGUNDA": [6, 7]}),
            Course("CLINC-B", "Clínica Médica de Cães e Gatos (Turma B)",
                   36, {"TERÇA": [7, 8]}),
            Course("CLINC-C", "Clínica Médica de Cães e Gatos (Turma C)",
                   36, {"QUARTA": [7, 8]}),
            Course("CLINC-D", "Clínica Médica de Cães e Gatos (Turma D)",
                   36, {"QUARTA": [6, 7]}),
            Course("FISREPO-TEO", "Fisiopatologia da Reprodução (Teórica)",
                   72, {"SEGUNDA": [6, 7, 8]}),
            Course("FISREPO-A", "Fisiopatologia da Reprodução (Turma A)",
                   36, {"TERÇA": [7, 8]}),
            Course("FISREPO-B", "Fisiopatologia da Reprodução (Turma B)",
                   36, {"TERÇA": [8, 9]}),
            Course("FISREPO-C", "Fisiopatologia da Reprodução (Turma C)",
                   36, {"QUARTA": [7, 8]}),
            Course("FISREPO-D", "Fisiopatologia da Reprodução (Turma D)",
                   36, {"QUINTA": [8, 9]}),
            Course("BOVIC-TEO", "Bovinocultura de Corte (Teórica)",
                   54, {"SEXTA": [1, 2]}),
            Course("BOVIC-A", "Bovinocultura de Corte (Turma A)",
                   36, {"SEXTA": [6, 7, 8]}),
            Course("SPUB-TEO", "Saúde Pública Veterinária (Teórica)",
                   54, {"SEXTA": [6, 7]}),
            Course("SPUB-A", "Saúde Pública Veterinária (Turma A)",
                   36, {"SEXTA": [8]}),
            Course("SPUB-B", "Saúde Pública Veterinária (Turma B)",
                   36, {"SEXTA": [9]}),

            # 8ª FASE
            Course("CLINE-TEO", "Clínica Médica de Equinos (Teórica)",
                   72, {"TERÇA": [0, 1, 2]}),
            Course("CLINE-A", "Clínica Médica de Equinos (Turma A)",
                   36, {"SEGUNDA": [0, 1]}),
            Course("CLINE-B", "Clínica Médica de Equinos (Turma B)",
                   36, {"QUARTA": [2, 3]}),
            Course("CLINE-C", "Clínica Médica de Equinos (Turma C)",
                   36, {"QUARTA": [8, 9]}),
            Course("CLINE-D", "Clínica Médica de Equinos (Turma D)",
                   36, {"SEXTA": [0, 1]}),
            Course("PATCL2-TEO", "Patologia e Clínica Cirúrgica (Teórica)",
                   72, {"QUARTA": [0, 1]}),
            Course("PATCL2-A", "Patologia e Clínica Cirúrgica (Turma A)",
                   36, {"SEGUNDA": [0, 1, 2, 3]}),
            Course("PATCL2-B", "Patologia e Clínica Cirúrgica (Turma B)",
                   36, {"TERÇA": [6, 7, 8]}),
            Course("PATCL2-C", "Patologia e Clínica Cirúrgica (Turma C)",
                   36, {"QUARTA": [0, 1, 2, 3]}),
            Course("PATCL2-D", "Patologia e Clínica Cirúrgica (Turma D)",
                   36, {"SEXTA": [0, 1, 2, 3]}),
            Course("BOVIL-8", "Bovinocultura de Leite",
                   54, {"SEGUNDA": [6, 7, 8]}),
            Course("SANSU-TEO", "Sanidade Suína (Teórica)",
                   54, {"TERÇA": [6, 7, 8]}),
            Course("SANSU-A", "Sanidade Suína (Turma A)", 36, {"QUARTA": [6]}),
            Course("SANSU-B", "Sanidade Suína (Turma B)", 36, {"QUARTA": [6]}),
            Course("SANSU-C", "Sanidade Suína (Turma C)", 36, {"QUARTA": [8]}),
            Course("INSPE-TEO", "Inspeção e Tech. Prod. Origem Anim. I",
                   72, {"SEGUNDA": [9, 10]}),
            Course("INSPE-A", "Inspeção e Tech. Origem Anim. I (Turma A)",
                   36, {"TERÇA": [9, 10]}),
            Course("INSPE-B", "Inspeção e Tech. Origem Anim. I (Turma B)",
                   36, {"TERÇA": [11, 12]}),
            Course("AVIC-TEO", "Avicultura (Teórica)", 54, {"QUARTA": [6, 7]}),
            Course("AVIC-A", "Avicultura (Turma A)", 36, {"QUARTA": [8]}),
            Course("AVIC-B", "Avicultura (Turma B)", 36, {"QUARTA": [8]}),
            Course("AVIC-C", "Avicultura (Turma C)", 36, {"QUARTA": [9]}),
            Course("OVINO-TEO", "Ovinocultura (Teórica)", 54, {"SEXTA": [6]}),
            Course("OVINO-A", "Ovinocultura (Turma A)", 36, {"SEXTA": [8]}),
            Course("OVINO-B", "Ovinocultura (Turma B)", 36, {"SEXTA": [8]}),

            # 9ª FASE
            Course("OBSTE-TEO", "Obstetrícia Veterinária (Teórica)",
                   54, {"SEGUNDA": [10, 11]}),
            Course("OBSTE-A", "Obstetrícia Veterinária (Turma A)",
                   36, {"SEGUNDA": [0, 1]}),
            Course("OBSTE-B", "Obstetrícia Veterinária (Turma B)",
                   36, {"SEGUNDA": [2, 3]}),
            Course("OBSTE-C", "Obstetrícia Veterinária (Turma C)",
                   36, {"SEGUNDA": [6, 7]}),
            Course("OBSTE-D", "Obstetrícia Veterinária (Turma D)",
                   36, {"SEGUNDA": [8, 9]}),
            Course("INSP2-TEO", "Inspeção e Tech. Prod. Origem Anim. II",
                   72, {"QUARTA": [0, 1]}),
            Course("INSP2-A", "Inspeção e Tech. Origem Anim. II (Turma A)",
                   36, {"QUARTA": [2, 3]}),
            Course("INSP2-B", "Inspeção e Tech. Origem Anim. II (Turma B)",
                   36, {"QUARTA": [6, 7]}),
            Course("INSP2-C", "Inspeção e Tech. Origem Anim. II (Turma C)",
                   36, {"QUARTA": [8, 9]}),
            Course("TOXI-9", "Toxicologia e Plantas Tóxicas",
                   54, {"TERÇA": [8, 9]}),
            Course("DAVES-TEO", "Doenças das Aves (Teórica)",
                   54, {"QUARTA": [8, 9]}),
            Course("DAVES-A", "Doenças das Aves (Turma A)",
                   36, {"SEXTA": [0, 1]}),
            Course("DAVES-B", "Doenças das Aves (Turma B)",
                   36, {"SEXTA": [2, 3]}),
            Course("DAVES-C", "Doenças das Aves (Turma C)",
                   36, {"QUARTA": [6, 7]}),

            # ELETIVAS
            Course("LACTI-EL", "Tecnologia de Lacticínios",
                   36, {"SEGUNDA": [2, 3]}),
            Course("CITO-EL", "Citologia Diagnóstica", 36, {"QUARTA": [2, 3]}),
            Course("DERMA-EL", "Dermatologia Veterinária",
                   36, {"SEXTA": [2, 3]}),
            Course("FISIA-EL", "Fisiatra Veterinária",
                   36, {"SEGUNDA": [6, 7]}),
            Course("GEREN-EL", "Gerenciamento e Projetos Agropecuários",
                   36, {"QUARTA": [6, 7]}),
            Course("MICRO-PESQ", "Microbiologia dos Pescados",
                   36, {"QUINTA": [6, 7]}),
            Course("EQUIN-EL", "Equinocultura", 36, {"QUINTA": [6, 7]}),
            Course("INSEM-EL", "Inseminação Artificial",
                   36, {"QUINTA": [6, 7]}),
            Course("BIOMOL-EL", "Biologia Molecular", 36, {"SEGUNDA": [8, 9]}),
            Course("CARDIO-EL", "Cardiologia de Cães e Gatos",
                   36, {"TERÇA": [8, 9]}),
            Course("MEDSEL-EL", "Medicina de Animais Selvagens",
                   36, {"QUARTA": [8, 9]}),
            Course("COMPBEM-EL", "Comportamento e Bem-Estar Animal II",
                   36, {"TERÇA": [10, 11]}),
            Course("ANALAL-EL", "Análise de Alimentos",
                   54, {"SEGUNDA": [11, 12, 13, 14]}),
            Course("LIBRAS-EL", "Libras", 36, {"SEGUNDA": [6, 7]}),
            Course("PECON-EL", "Animais Peçonhentos", 36, {"SEGUNDA": [8, 9]}),
        ]

    # --- UI & Layout ---
    def _build_menu(self):
        menubar = tk.Menu(self.root)
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Sair", command=self.root.quit)
        menubar.add_cascade(label="Arquivo", menu=file_menu)
        self.root.config(menu=menubar)

    def _build_layout(self):
        paned = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        paned.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Painel Esquerdo
        left_frame = ttk.Frame(paned, padding=5)
        paned.add(left_frame, weight=1)

        ttk.Label(left_frame, text="Pesquisar:", font=(
            "Helvetica", 10, "bold")).pack(anchor=tk.W, pady=(0, 2))

        self.search_var.trace_add(
            "write", lambda *args: self.update_course_list())
        search_entry = ttk.Entry(left_frame, textvariable=self.search_var)
        search_entry.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(left_frame, text=" Todas as Disciplinas Med Vet CAV:",
                  font=("Helvetica", 10, "bold")).pack(anchor=tk.W)
        self.catalog_listbox = tk.Listbox(
            left_frame, selectmode=tk.SINGLE, height=12)
        self.catalog_listbox.pack(fill=tk.BOTH, expand=True, pady=(0, 5))
        self.catalog_listbox.bind("<<ListboxSelect>>", self.on_course_select)

        self.details_label = ttk.Label(
            left_frame, text="Selecione uma disciplina para detalhes.", wraplength=280, justify=tk.LEFT)
        self.details_label.pack(fill=tk.X, pady=5)

        btn_frame = ttk.Frame(left_frame)
        btn_frame.pack(fill=tk.X, pady=5)

        ttk.Button(btn_frame, text="Adicionar Disciplina", command=self.register_selected_course).pack(
            side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 2))
        ttk.Button(btn_frame, text="+ Customizada", command=self.open_custom_course_dialog).pack(
            side=tk.RIGHT, fill=tk.X, expand=True, padx=(2, 0))

        ttk.Label(left_frame, textvariable=self.registered_count_var, font=(
            "Helvetica", 10, "bold")).pack(anchor=tk.W, pady=(10, 2))
        self.registered_listbox = tk.Listbox(
            left_frame, selectmode=tk.SINGLE, height=8)
        self.registered_listbox.pack(fill=tk.BOTH, expand=True, pady=(0, 5))

        ttk.Button(left_frame, text="Remover Disciplina Selecionada",
                   command=self.drop_selected_course).pack(fill=tk.X)

        # Painel Direito (Grade)
        right_frame = ttk.Frame(paned, padding=5)
        paned.add(right_frame, weight=3)

        ttk.Label(right_frame, text="Planejador Semanal de Horários - UDESC CAV",
                  font=("Helvetica", 12, "bold")).pack(anchor=tk.W, pady=(0, 5))

        canvas_container = ttk.Frame(right_frame)
        canvas_container.pack(fill=tk.BOTH, expand=True)

        self.canvas = tk.Canvas(canvas_container, bg="white")
        scrollbar = ttk.Scrollbar(
            canvas_container, orient=tk.VERTICAL, command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # --- Lógica do Sistema ---
    def update_registered_count(self):
        count = len(self.registered_courses)
        self.registered_count_var.set(f"Disciplinas Selecionadas ({count}):")

    def update_course_list(self):
        query = self.search_var.get().lower().strip()
        self.catalog_listbox.delete(0, tk.END)
        self.filtered_courses = []

        for course in self.available_courses:
            if query in course.code.lower() or query in course.name.lower() or query in str(course.credits):
                self.filtered_courses.append(course)
                self.catalog_listbox.insert(tk.END, str(course))

    def on_course_select(self, event):
        sel = self.catalog_listbox.curselection()
        if not sel:
            return
        idx = sel[0]
        course = self.filtered_courses[idx]

        details = f"Código: {course.code}\nNome: {course.name}\nCarga Horária: {course.credits}h\nHorários:\n"
        for day, slots in course.schedule.items():
            slot_str = ", ".join([get_slot_time_str(s) for s in slots])
            details += f"  • {day}: {slot_str}\n"
        self.details_label.config(text=details)

    def check_conflict(self, course_to_add: Course) -> Optional[str]:
        for reg in self.registered_courses:
            for day, slots in course_to_add.schedule.items():
                if day in reg.schedule:
                    overlap = set(slots).intersection(set(reg.schedule[day]))
                    if overlap:
                        conflicting_slot = sorted(list(overlap))[0]
                        return f"Conflito com '{reg.name}' na {day} no horário {get_slot_time_str(conflicting_slot)}."
        return None

    def register_selected_course(self):
        sel = self.catalog_listbox.curselection()
        if not sel:
            messagebox.showwarning(
                "Aviso", "Selecione uma disciplina do catálogo para adicionar.")
            return

        course = self.filtered_courses[sel[0]]

        if course in self.registered_courses:
            messagebox.showinfo("Aviso", f"'{course.name}' já foi adicionada.")
            return

        conflict_msg = self.check_conflict(course)
        if conflict_msg:
            messagebox.showerror("Conflito de Horário", conflict_msg)
            return

        self.registered_courses.append(course)
        self.registered_listbox.insert(tk.END, str(course))
        self.draw_schedule_grid()
        self.update_registered_count()
        messagebox.showinfo(
            "Sucesso", f"'{course.name}' adicionada com sucesso!")

    def drop_selected_course(self):
        sel = self.registered_listbox.curselection()
        if not sel:
            messagebox.showwarning(
                "Aviso", "Selecione uma disciplina na lista para remover.")
            return

        idx = sel[0]
        self.registered_courses.pop(idx)
        self.registered_listbox.delete(idx)
        self.draw_schedule_grid()
        self.update_registered_count()

    # --- Renderização Visual ---
    def draw_schedule_grid(self):
        self.canvas.delete("all")

        col_width = 130
        row_height = 35
        header_height = 30
        time_col_width = 110

        self.canvas.create_rectangle(
            0, 0, time_col_width, header_height, fill="#faf1f1", outline="#cccccc")
        self.canvas.create_text(time_col_width / 2, header_height / 2,
                                text="Horários", font=("Helvetica", 9, "bold"))

        for i, day in enumerate(DAYS):
            x1 = time_col_width + (i * col_width)
            x2 = x1 + col_width
            self.canvas.create_rectangle(
                x1, 0, x2, header_height, fill="#e1e1e1", outline="#cccccc")
            self.canvas.create_text(
                (x1 + x2) / 2, header_height / 2, text=day, font=("Helvetica", 9, "bold"))

        for slot_idx in range(TOTAL_SLOTS):
            y1 = header_height + (slot_idx * row_height)
            y2 = y1 + row_height

            self.canvas.create_rectangle(
                0, y1, time_col_width, y2, fill="#c2dbf5", outline="#cccccc")
            self.canvas.create_text(time_col_width / 2, (y1 + y2) / 2,
                                    text=get_slot_time_str(slot_idx), font=("Helvetica", 8))

            for day_idx in range(len(DAYS)):
                x1 = time_col_width + (day_idx * col_width)
                x2 = x1 + col_width
                self.canvas.create_rectangle(
                    x1, y1, x2, y2, fill="white", outline="#eeeeee")

        bg_green = "#2ecc71"
        border_green = "#27ae60"

        for course in self.registered_courses:
            for day, slots in course.schedule.items():
                if day not in DAYS:
                    continue
                day_idx = DAYS.index(day)
                x1 = time_col_width + (day_idx * col_width) + 2
                x2 = x1 + col_width - 4

                for slot in slots:
                    if slot >= TOTAL_SLOTS:
                        continue
                    y1 = header_height + (slot * row_height) + 2
                    y2 = y1 + row_height - 4

                    self.canvas.create_rectangle(
                        x1, y1, x2, y2, fill=bg_green, outline=border_green, width=1.5)
                    self.canvas.create_text(
                        (x1 + x2) / 2,
                        (y1 + y2) / 2,
                        text=f"{course.code}\n{course.name[:14]}...",
                        fill="white",
                        font=("Helvetica", 7, "bold"),
                        justify=tk.CENTER,
                    )

        total_height = header_height + (TOTAL_SLOTS * row_height)
        total_width = time_col_width + (len(DAYS) * col_width)
        self.canvas.config(scrollregion=(0, 0, total_width, total_height))

    # --- Diálogo Customizado ---
    def open_custom_course_dialog(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Adicionar Matéria Personalizada")
        dialog.geometry("380x420")
        dialog.grab_set()

        ttk.Label(dialog, text="Código:").pack(
            anchor=tk.W, padx=10, pady=(10, 0))
        code_entry = ttk.Entry(dialog)
        code_entry.pack(fill=tk.X, padx=10)

        ttk.Label(dialog, text="Nome da Matéria:").pack(
            anchor=tk.W, padx=10, pady=(5, 0))
        name_entry = ttk.Entry(dialog)
        name_entry.pack(fill=tk.X, padx=10)

        ttk.Label(dialog, text="Carga Horária:").pack(
            anchor=tk.W, padx=10, pady=(5, 0))
        credits_entry = ttk.Entry(dialog)
        credits_entry.pack(fill=tk.X, padx=10)

        ttk.Label(dialog, text="Dia da Semana:").pack(
            anchor=tk.W, padx=10, pady=(5, 0))
        day_combo = ttk.Combobox(dialog, values=DAYS, state="readonly")
        day_combo.set(DAYS[0])
        day_combo.pack(fill=tk.X, padx=10)

        ttk.Label(dialog, text="Selecione os Slots (Segure Ctrl para múltiplos):").pack(
            anchor=tk.W, padx=10, pady=(5, 0))
        slot_listbox = tk.Listbox(dialog, selectmode=tk.MULTIPLE, height=6)
        for s in range(TOTAL_SLOTS):
            slot_listbox.insert(tk.END, f"Slot {s}: {get_slot_time_str(s)}")
        slot_listbox.pack(fill=tk.X, padx=10)

        def save_course():
            code = code_entry.get().strip()
            name = name_entry.get().strip()
            try:
                credits = int(credits_entry.get().strip())
            except ValueError:
                messagebox.showerror(
                    "Erro", "Carga horária precisa ser número inteiro.")
                return

            selected_slots = slot_listbox.curselection()
            if not code or not name or not selected_slots:
                messagebox.showerror("Erro", "Preencha todos os campos.")
                return

            day = day_combo.get()
            schedule = {day: list(selected_slots)}

            new_course = Course(code, name, credits, schedule)
            self.available_courses.append(new_course)
            self.update_course_list()
            dialog.destroy()
            messagebox.showinfo(
                "Sucesso", f"Matéria '{code}' criada e adicionada ao catálogo.")

        ttk.Button(dialog, text="Salvar Matéria",
                   command=save_course).pack(pady=15)


# --- Execução ---
if __name__ == "__main__":
    root = tk.Tk()
    app = CoursePlannerApp(root)
    root.mainloop()
