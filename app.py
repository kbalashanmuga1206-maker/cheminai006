import io
import os
import streamlit as st
import pandas as pd
from datetime import datetime

from rdkit import Chem
from rdkit.Chem import (
    AllChem, Descriptors, Crippen, Lipinski,
    Draw, rdMolDescriptors
)

st.set_page_config(
    page_title="Molecule Studio AI",
    page_icon="🧪",
    layout="wide"
)

# ---------------- DESIGN ----------------

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Poppins', sans-serif;
}

.stApp {
    background: linear-gradient(135deg,#eef2ff,#f0f9ff,#faf5ff);
}

.hero {
    background: linear-gradient(120deg,#172554,#4f46e5,#9333ea);
    padding: 30px;
    border-radius: 22px;
    color: white;
    margin-bottom: 25px;
}

.hero h1 {
    font-size: 36px;
    font-weight: 800;
}

div[data-testid="stMetric"] {
    background: white;
    padding: 15px;
    border-radius: 15px;
    border: 1px solid #ddd;
}

.stButton button {
    border-radius: 12px;
    font-weight: bold;
    min-height: 45px;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
<h1>🧪 Molecule Studio AI</h1>
<p>Advanced AI Chemistry Laboratory | Version 2.0</p>
<p>Explore • Analyze • Visualize • Learn</p>
</div>
""", unsafe_allow_html=True)

# ---------------- SAMPLE MOLECULES ----------------

SAMPLES = {
    "Caffeine": "Cn1c(=O)c2c(ncn2C)n(C)c1=O",
    "Aspirin": "CC(=O)OC1=CC=CC=C1C(=O)O",
    "Paracetamol": "CC(=O)NC1=CC=C(O)C=C1",
    "Ibuprofen": "CC(C)CC1=CC=C(C=C1)C(C)C(=O)O",
    "Benzene": "c1ccccc1",
    "Ethanol": "CCO",
    "Glucose": "C(C1C(C(C(C(O1)O)O)O)O)O"
}

def get_molecule(smiles):
    if not smiles.strip():
        return None
    return Chem.MolFromSmiles(smiles.strip())

def calculate_properties(mol):
    return {
        "Molecular Formula":
            rdMolDescriptors.CalcMolFormula(mol),

        "Molecular Weight":
            round(Descriptors.MolWt(mol), 3),

        "Exact Mass":
            round(Descriptors.ExactMolWt(mol), 4),

        "LogP":
            round(Crippen.MolLogP(mol), 3),

        "TPSA":
            round(rdMolDescriptors.CalcTPSA(mol), 3),

        "H Bond Donors":
            Lipinski.NumHDonors(mol),

        "H Bond Acceptors":
            Lipinski.NumHAcceptors(mol),

        "Rotatable Bonds":
            Lipinski.NumRotatableBonds(mol),

        "Heavy Atoms":
            mol.GetNumHeavyAtoms(),

        "Aromatic Rings":
            rdMolDescriptors.CalcNumAromaticRings(mol),

        "Fraction Csp3":
            round(rdMolDescriptors.CalcFractionCSP3(mol), 3)
    }

# ---------------- PDF REPORT ----------------

def create_pdf(name, smiles, props):
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import A4
    from reportlab.platypus import (
        SimpleDocTemplate, Paragraph, Spacer, Table,
        TableStyle
    )
    from reportlab.lib.styles import getSampleStyleSheet

    buffer = io.BytesIO()
    document = SimpleDocTemplate(buffer, pagesize=A4)
    styles = getSampleStyleSheet()

    content = [
        Paragraph("MOLECULE STUDIO AI", styles["Title"]),
        Spacer(1, 15),
        Paragraph(f"Molecule: {name}", styles["Heading2"]),
        Paragraph(f"SMILES: {smiles}", styles["BodyText"]),
        Paragraph(
            f"Generated: {datetime.now().strftime('%d-%m-%Y %H:%M')}",
            styles["BodyText"]
        ),
        Spacer(1, 20)
    ]

    data = [["Property", "Value"]]
    data += [[str(k), str(v)] for k, v in props.items()]

    table = Table(data)
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.darkblue),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("PADDING", (0, 0), (-1, -1), 8)
    ]))

    content.append(table)
    document.build(content)

    return buffer.getvalue()

# ---------------- SIDEBAR ----------------

page = st.sidebar.radio(
    "🧭 Laboratory Menu",
    [
        "Dashboard",
        "Molecule Explorer",
        "Molecule Comparison",
        "AI Chemistry Tutor",
        "3D Laboratory",
        "Chemistry Quiz",
        "About"
    ]
)

st.sidebar.markdown("---")
st.sidebar.caption("Molecule Studio AI V2.0")

# ---------------- DASHBOARD ----------------

if page == "Dashboard":

    st.title("🏠 Laboratory Dashboard")

    a, b, c = st.columns(3)

    a.metric("Available Samples", "7")
    b.metric("Laboratory Version", "2.0")
    c.metric("Analysis Engine", "RDKit")

    st.subheader("Laboratory Features")

    features = [
        "🔬 SMILES Validation",
        "🧬 Molecular Properties",
        "📊 Molecule Comparison",
        "🤖 AI Chemistry Tutor",
        "🌐 3D Molecular Coordinates",
        "📄 PDF Research Reports",
        "🧠 Chemistry Assessment"
    ]

    for feature in features:
        st.success(feature)

# ---------------- MOLECULE EXPLORER ----------------

elif page == "Molecule Explorer":

    st.title("🔬 Molecule Explorer")

    sample = st.selectbox(
        "Choose a sample molecule",
        ["Custom"] + list(SAMPLES.keys())
    )

    default = "" if sample == "Custom" else SAMPLES[sample]

    name = st.text_input(
        "Molecule Name",
        sample if sample != "Custom" else "My Molecule"
    )

    smiles = st.text_area(
        "Enter SMILES",
        default,
        height=100
    )

    if st.button("🚀 Analyze Molecule", type="primary"):

        mol = get_molecule(smiles)

        if mol is None:
            st.error("Invalid SMILES. Please check your input.")

        else:
            st.success("SMILES validation successful!")

            st.subheader("2D Molecular Structure")

            st.image(
                Draw.MolToImage(mol, size=(700, 450)),
                use_container_width=True
            )

            props = calculate_properties(mol)

            st.subheader("Molecular Properties")

            cols = st.columns(4)

            cols[0].metric(
                "Molecular Weight",
                props["Molecular Weight"]
            )

            cols[1].metric(
                "LogP",
                props["LogP"]
            )

            cols[2].metric(
                "TPSA",
                props["TPSA"]
            )

            cols[3].metric(
                "Heavy Atoms",
                props["Heavy Atoms"]
            )

            st.dataframe(
                pd.DataFrame(
                    list(props.items()),
                    columns=["Property", "Value"]
                ),
                use_container_width=True
            )

            st.code(
                Chem.MolToSmiles(mol),
                language="text"
            )

            pdf = create_pdf(name, smiles, props)

            st.download_button(
                "📄 Download PDF Report",
                pdf,
                file_name="molecule_report.pdf",
                mime="application/pdf"
            )

# ---------------- COMPARISON ----------------

elif page == "Molecule Comparison":

    st.title("⚖️ Molecule Comparison")

    count = st.slider(
        "Number of molecules",
        2, 6, 2
    )

    molecules = []

    for i in range(count):

        with st.expander(f"Molecule {i+1}", expanded=True):

            sample = st.selectbox(
                f"Sample {i+1}",
                ["Custom"] + list(SAMPLES.keys()),
                key=f"sample_{i}"
            )

            smiles = st.text_input(
                f"SMILES {i+1}",
                SAMPLES[sample] if sample != "Custom" else "",
                key=f"smiles_{i}"
            )

            name = st.text_input(
                f"Name {i+1}",
                sample if sample != "Custom" else f"Molecule {i+1}",
                key=f"name_{i}"
            )

            molecules.append((name, smiles))

    if st.button("Compare All Molecules", type="primary"):

        rows = {}
        valid = True

        for name, smiles in molecules:

            mol = get_molecule(smiles)

            if mol is None:
                st.error(f"Invalid SMILES for {name}")
                valid = False
                break

            rows[name] = calculate_properties(mol)

        if valid:

            st.dataframe(
                pd.DataFrame(rows),
                use_container_width=True
            )

            cols = st.columns(count)

            for i, (name, smiles) in enumerate(molecules):
                mol = get_molecule(smiles)

                with cols[i]:
                    st.image(
                        Draw.MolToImage(mol),
                        caption=name,
                        use_container_width=True
                    )

# ---------------- AI CHEMISTRY TUTOR ----------------

elif page == "AI Chemistry Tutor":

    st.title("🤖 AI Chemistry Tutor")

    st.write(
        "Ask questions about chemistry, molecular structures, "
        "SMILES, chemical bonds and molecular properties."
    )

    api_key = st.secrets.get(
        "OPENAI_API_KEY",
        os.getenv("OPENAI_API_KEY", "")
    )

    if not api_key:
        st.warning(
            "Add your OpenAI API key in Streamlit Secrets "
            "to activate the AI Chemistry Tutor."
        )

    if "chat" not in st.session_state:
        st.session_state.chat = []

    for msg in st.session_state.chat:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    prompt = st.chat_input("Ask your chemistry question...")

    if prompt:

        st.session_state.chat.append({
            "role": "user",
            "content": prompt
        })

        with st.chat_message("user"):
            st.write(prompt)

        if api_key:
            try:
                from openai import OpenAI

                client = OpenAI(api_key=api_key)

                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {
                            "role": "system",
                            "content": (
                                "You are Molecule Studio AI, a careful "
                                "university-level chemistry tutor. "
                                "Explain concepts clearly and accurately. "
                                "Do not claim molecular descriptors prove "
                                "drug safety or biological effectiveness."
                            )
                        },
                        *st.session_state.chat[-10:]
                    ],
                    max_tokens=900
                )

                answer = response.choices[0].message.content

            except Exception as e:
                answer = f"AI error: {e}"

        else:
            answer = (
                "AI is not connected. Add OPENAI_API_KEY in "
                "Streamlit Secrets to activate live AI answers."
            )

        st.session_state.chat.append({
            "role": "assistant",
            "content": answer
        })

        with st.chat_message("assistant"):
            st.markdown(answer)

# ---------------- 3D LABORATORY ----------------

elif page == "3D Laboratory":

    st.title("🌐 3D Molecular Laboratory")

    smiles = st.text_input(
        "Enter molecular SMILES",
        "CCO"
    )

    if st.button("Generate 3D Structure"):

        mol = get_molecule(smiles)

        if mol is None:
            st.error("Invalid SMILES")

        else:
            mol3d = Chem.AddHs(mol)

            status = AllChem.EmbedMolecule(
                mol3d,
                randomSeed=42
            )

            if status == 0:

                AllChem.UFFOptimizeMolecule(mol3d)

                st.success("3D coordinates generated!")

                mol_block = Chem.MolToMolBlock(mol3d)

                st.download_button(
                    "Download 3D MOL File",
                    mol_block,
                    file_name="molecule_3d.mol",
                    mime="chemical/x-mdl-molfile"
                )

                st.info(
                    "This version generates and exports 3D coordinates. "
                    "A live interactive 3D viewer can be added using 3Dmol.js."
                )

            else:
                st.error("3D coordinate generation failed.")

# ---------------- QUIZ ----------------

elif page == "Chemistry Quiz":

    st.title("🧠 Chemistry Knowledge Test")

    questions = [
        (
            "Which notation represents molecular structures as text?",
            ["SMILES", "HTML", "CSV", "JPEG"],
            "SMILES"
        ),
        (
            "What does LogP estimate?",
            ["Lipophilicity", "Molecular colour", "Atom number", "pH"],
            "Lipophilicity"
        ),
        (
            "Which library provides cheminformatics tools?",
            ["RDKit", "Flask", "Django", "Tkinter"],
            "RDKit"
        ),
        (
            "What is TPSA?",
            [
                "Topological Polar Surface Area",
                "Total Protein Sequence Analysis",
                "Thermal Pressure Scale",
                "None"
            ],
            "Topological Polar Surface Area"
        ),
        (
            "What is molecular weight commonly measured in?",
            ["g/mol", "metres", "litres", "seconds"],
            "g/mol"
        )
    ]

    answers = []

    for i, (question, options, correct) in enumerate(questions):

        answer = st.radio(
            f"{i+1}. {question}",
            options,
            key=f"question_{i}"
        )

        answers.append(answer)

    if st.button("Submit Quiz", type="primary"):

        score = sum(
            answers[i] == questions[i][2]
            for i in range(len(questions))
        )

        st.success(
            f"Your score: {score}/{len(questions)}"
        )

        st.progress(score / len(questions))

# ---------------- ABOUT ----------------

elif page == "About":

    st.title("About Molecule Studio AI")

    st.markdown("""
    ### Version 2.0

    An educational AI chemistry laboratory for students.

    **Technologies**

    - Python
    - Streamlit
    - RDKit
    - Pandas
    - OpenAI API
    - ReportLab

    **Developer**

    K. Balashanmuga

    AIML Student

    SRM Institute of Science and Technology
    """)

    st.info(
        "Educational application. Computational predictions "
        "are not experimental or medical evidence."
    )

st.markdown("---")
st.caption(
    "Molecule Studio AI V2.0 | Educational Chemistry Laboratory"
)
