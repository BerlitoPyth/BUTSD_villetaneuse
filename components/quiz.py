import streamlit as st
import streamlit.components.v1 as components
import sys
from pathlib import Path

# Ajout du chemin absolu au PYTHONPATH
file_path = Path(__file__).resolve()
project_root = file_path.parent.parent  # Remonte d'un niveau pour atteindre la racine du projet
sys.path.append(str(project_root))

__all__ = ['display_quiz']  # Export explicite de la fonction

def display_quiz():
    quiz_html = """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <script src="https://unpkg.com/react@17/umd/react.production.min.js"></script>
        <script src="https://unpkg.com/react-dom@17/umd/react-dom.production.min.js"></script>
        <script src="https://unpkg.com/babel-standalone@6/babel.min.js"></script>
        <style>
            /* Reset et base */
            * { margin: 0; padding: 0; box-sizing: border-box; }
            
            body {
                background: transparent;
                font-family: system-ui, -apple-system, sans-serif;
                color: #fff;
                line-height: 1.2;
                padding: 0.5rem;
            }

            /* Container principal plus grand */
            .quiz-wrapper {
                max-width: 1360px;  /* +70% */
                min-height: 680px;  /* +70% de la hauteur originale de 400px */
                margin: 0 auto;
            }

            /* Card du quiz plus grande */
            .quiz-card {
                background: rgba(15, 23, 42, 0.6);
                border-radius: 6px;
                padding: 1.7rem;  /* +70% */
                min-height: 680px;  /* +70% */
                border: 1px solid rgba(255, 255, 255, 0.1);
            }

            /* En-tête compact */
            .quiz-header {
                margin-bottom: 0.5rem;
            }

            /* Titres et textes plus grands */
            .quiz-title {
                font-size: 1.7rem;  /* +70% */
                margin-bottom: 0.85rem;
                color: rgba(255, 255, 255, 0.9);
            }

            .quiz-progress {
                font-size: 1.36rem;  /* +70% */
                color: rgba(255, 255, 255, 0.6);
            }

            /* Barre de progression minimale */
            .progress-bar {
                height: 5px;  /* +70% */
                background: rgba(255, 255, 255, 0.1);
                margin: 0.6rem 0;
            }

            .progress-fill {
                height: 100%;
                background: #3B82F6;
                transition: width 0.3s ease;
            }

            /* Question compacte */
            .question {
                margin: 0.5rem 0;
            }

            .question-title {
                font-size: 1.53rem;  /* +70% */
                margin-bottom: 0.85rem;
                color: rgba(255, 255, 255, 0.9);
            }

            .question-text {
                font-size: 1.45rem;  /* +70% */
                color: rgba(255, 255, 255, 0.8);
                margin-bottom: 1.28rem;
            }

            /* Boutons de réponse plus grands */
            .answer-button {
                width: 100%;
                padding: 1.28rem 1.7rem;  /* +70% */
                margin: 0.51rem 0;
                background: rgba(59, 130, 246, 0.1);
                border: 1px solid rgba(59, 130, 246, 0.2);
                border-radius: 4px;
                color: white;
                font-size: 1.45rem;  /* +70% */
                cursor: pointer;
                transition: all 0.2s ease;
                display: flex;
                align-items: center;
                gap: 0.68rem;
                min-height: 4.25rem;  /* +70% */
            }

            /* Résultats plus grands */
            .results {
                padding: 1.28rem;  /* +70% */
                min-height: 680px;  /* +70% */
            }

            .result-header {
                font-size: 1.45rem;  /* +70% */
                text-align: center;
                margin-bottom: 0.85rem;
                padding: 0.68rem;
                background: rgba(59, 130, 246, 0.1);
                border-radius: 4px;
            }

            .result-item {
                padding: 0.68rem 1.02rem;  /* +70% */
                margin: 0.34rem 0;
                font-size: 1.36rem;  /* +70% */
                border-radius: 4px;
                background: rgba(59, 130, 246, 0.08);
                display: flex;
                gap: 0.85rem;
                align-items: flex-start;
            }

            /* Icônes plus grandes */
            .icon {
                width: 2.04rem;  /* +70% */
                height: 2.04rem;  /* +70% */
                flex-shrink: 0;
            }

            .chevron-icon {
                width: 1.36rem;  /* +70% */
                height: 1.36rem;  /* +70% */
            }

            /* Styles des résultats avec couleurs */
            .result-item .icon {
                width: 2.04rem;  /* +70% */
                height: 2.04rem;  /* +70% */
            }

            .icon-yellow {
                color: #FBBF24;
                stroke: #FBBF24;
            }

            .icon-blue {
                color: #60A5FA;
                stroke: #60A5FA;
            }

            .icon-purple {
                color: #A78BFA;
                stroke: #A78BFA;
            }

            .icon-green {
                color: #34D399;
                stroke: #34D399;
            }

            .icon-red {
                color: #F87171;
                stroke: #F87171;
            }

            /* Card du quiz plus compacte pendant les questions */
            .quiz-card {
                background: rgba(15, 23, 42, 0.6);
                border-radius: 6px;
                padding: 1.7rem;
                border: 1px solid rgba(255, 255, 255, 0.1);
                height: fit-content;  /* S'adapte au contenu */
                min-height: auto;    /* Supprime la hauteur minimale fixe */
            }

            /* Container du quiz plus compact pendant les questions */
            .quiz-wrapper {
                max-width: 1360px;
                margin: 0 auto;
                min-height: auto;    /* Supprime la hauteur minimale fixe */
                height: fit-content;  /* S'adapte au contenu */
            }

            /* Container des résultats - garde une hauteur fixe */
            .results {
                padding: 1.28rem;
                min-height: 680px;  /* Garde la hauteur minimale pour les résultats */
            }

            /* Ajustement de l'espacement des questions */
            .question {
                margin: 0.5rem 0;
                padding-bottom: 0.5rem;  /* Réduit l'espace en bas */
            }

            /* Ajustement des boutons de réponse */
            .space-y-3 {
                margin-bottom: 0;  /* Supprime la marge en bas */
            }

            .answer-button:last-child {
                margin-bottom: 0;  /* Supprime la marge du dernier bouton */
            }

        </style>
    </head>
    <body>
        <div id="quiz-root"></div>
        <script type="text/babel">
            // Composants d'icônes
            const Star = () => (
                <svg className="icon text-yellow-400" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                    <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/>
                </svg>
            );

            const Heart = () => (
                <svg className="icon text-red-400" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                    <path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"/>
                </svg>
            );

            const Brain = () => (
                <svg className="icon text-purple-400" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                    <path d="M9.5 2A2.5 2.5 0 0 1 12 4.5v15a2.5 2.5 0 0 1-4.96.44 2.5 2.5 0 0 1-2.04-.2 2.5 2.5 0 0 1 1-4.74 2.5 2.5 0 0 1 1.5-4.5 2.5 2.5 0 0 1 1.5-4.5Z"/>
                    <path d="M14.5 2A2.5 2.5 0 0 0 12 4.5v15a2.5 2.5 0 0 0 4.96.44 2.5 2.5 0 0 0 2.04-.2 2.5 2.5 0 0 0-1-4.74 2.5 2.5 0 0 0-1.5-4.5 2.5 2.5 0 0 0-1.5-4.5Z"/>
                </svg>
            );

            const Code = () => (
                <svg className="icon text-blue-400" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                    <polyline points="16 18 22 12 16 6"/>
                    <polyline points="8 6 2 12 8 18"/>
                </svg>
            );

            const Trophy = () => (
                <svg className="icon text-green-400" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                    <path d="M6 9H4.5a2.5 2.5 0 0 1 0-5H6"/>
                    <path d="M18 9h1.5a2.5 2.5 0 0 0 0-5H18"/>
                    <path d="M4 22h16"/>
                    <path d="M10 14.66V17c0 .55-.47.98-.97 1.21C7.85 18.75 7 20.24 7 22"/>
                    <path d="M14 14.66V17c0 .55.47.98.97 1.21C16.15 18.75 17 20.24 17 22"/>
                    <path d="M18 2H6v7a6 6 0 0 0 12 0V2Z"/>
                </svg>
            );

            const Lightbulb = () => (
                <svg className="icon text-yellow-400" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                    <path d="M15 14c.2-1 .7-1.7 1.5-2.5 1-.9 1.5-2.2 1.5-3.5A6 6 0 0 0 6 8c0 1 .2 2.2 1.5 3.5.7.7 1.3 1.5 1.5 2.5"/>
                    <path d="M9 18h6"/>
                    <path d="M10 22h4"/>
                </svg>
            );

            const ChevronRight = () => (
                <svg className="chevron-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                    <polyline points="9 18 15 12 9 6"/>
                </svg>
            );
            
            const Quiz = () => {
                const [currentStep, setCurrentStep] = React.useState(0);
                const [score, setScore] = React.useState(0);
                const [showResults, setShowResults] = React.useState(false);

                const questions = [
                    {
                        title: "La Passion & Motivation",
                        question: "Quel type d'étudiant recherchez-vous ?",
                        options: [
                            {
                                text: "Quelqu'un qui suit simplement le programme",
                                points: 0
                            },
                            {
                                text: "Un passionné qui s'investit au-delà des attentes avec détermination",
                                points: 1,
                                match: "Ma passion se reflète dans mes projets personnels (comme cette app par exemple). Je m'investis toujours à 100% dans ce qui me passionne."
                            }
                        ]
                    },
                    {
                        title: "L'Esprit d'Équipe",
                        question: "Quelle approche privilégiez-vous pour les projets collaboratifs ?",
                        options: [
                            {
                                text: "Une approche individualiste",
                                points: 0
                            },
                            {
                                text: "Une forte capacité à travailler en équipe et à tirer les autres vers le haut",
                                points: 1,
                                match: "Mon expérience de plongeur scaphandrier m'a appris l'importance du travail d'équipe. Cette compétence, combinée à ma passion pour le partage de connaissances, fait de moi un excellent coéquipier."
                            }
                        ]
                    },
                    {
                        title: "L'Engagement",
                        question: "Quel niveau d'investissement attendez-vous ?",
                        options: [
                            {
                                text: "Se contenter du minimum requis",
                                points: 0
                            },
                            {
                                text: "Un investissement total dans les projets",
                                points: 1,
                                match: "Je ne compte pas mes heures quand il s'agit d'apprendre et de progresser. Que ce soit dans les études ou dans mes projets personnels, je donne toujours le meilleur de moi-même."
                            }
                        ]
                    },
                    {
                        title: "L'Initiative",
                        question: "Quelle attitude privilégiez-vous face aux défis ?",
                        options: [
                            {
                                text: "Attendre les consignes",
                                points: 0
                            },
                            {
                                text: "Prendre des initiatives et chercher des solutions",
                                points: 1,
                                match: "Ma reconversion démontre ma capacité à prendre des initiatives. Je n'hésite pas à me lancer dans des projets ambitieux, comme l'apprentissage autodidacte de la programmation ou la création de nouvelles choses."
                            }
                        ]
                    },
                    {
                        title: "L'Excellence",
                        question: "Quelle approche de l'apprentissage recherchez-vous ?",
                        options: [
                            {
                                text: "Viser la moyenne",
                                points: 0
                            },
                            {
                                text: "Viser l'excellence et le dépassement de soi",
                                points: 1,
                                match: "Que ce soit dans le milieu professionnel, dans mes projets personnels ou dans le sport je vise toujours l'excellence. Mon objectif est de toujours m'améliorer et de repousser mes limites."
                            }
                        ]
                    }
                ];

                const handleAnswer = (points) => {
                    setScore(score + points);
                    if (currentStep < questions.length - 1) {
                        setCurrentStep(currentStep + 1);
                    } else {
                        setShowResults(true);
                    }
                };

                if (showResults) {
                    return <MatchProfile score={score} questions={questions} />;
                }

                return (
                    <div className="quiz-wrapper">
                        <div className="quiz-card">
                            <div className="quiz-header">
                                <div className="quiz-title">Trouvez le profil idéal</div>
                                <div className="quiz-progress">Question {currentStep + 1}/{questions.length}</div>
                                <div className="progress-bar">
                                    <div 
                                        className="progress-fill"
                                        style={{ width: `${((currentStep + 1) / questions.length) * 100}%` }}
                                    />
                                </div>
                            </div>

                            <div className="question fade-in">
                                <h3 className="question-title">
                                    {questions[currentStep].title}
                                </h3>
                                <p className="question-text">
                                    {questions[currentStep].question}
                                </p>
                                
                                <div className="space-y-3">
                                    {questions[currentStep].options.map((option, index) => (
                                        <button
                                            key={index}
                                            className="answer-button"
                                            onClick={() => handleAnswer(option.points)}
                                        >
                                            <ChevronRight />
                                            <span>{option.text}</span>
                                        </button>
                                    ))}
                                </div>
                            </div>
                        </div>
                    </div>
                );
            };

            const MatchProfile = ({ score, questions }) => {
                const matches = questions.filter((q, i) => score > i).map(q => q.options[1].match);
                const icons = [Star, Brain, Code, Trophy, Lightbulb];
                
                const percentage = (score / questions.length) * 100;
                const getMessage = () => {
                    if (percentage === 100) {
                        return "✨ Perfect Match ! Voici pourquoi je suis le candidat idéal";
                    } else if (percentage >= 80) {
                        return "🎯 Excellent ! Découvrez comment je corresponds à vos attentes";
                    } else {
                        return "Voici comment je peux répondre à vos critères";
                    }
                };
                
                return (
                    <div className="results">
                        <div className="result-header">{getMessage()}</div>
                        <div className="space-y-3">
                            {matches.map((match, index) => {
                                const iconClasses = [
                                    "icon-yellow",
                                    "icon-blue",
                                    "icon-purple",
                                    "icon-green",
                                    "icon-red"
                                ][index % 5];
                                return (
                                    <div key={index} className="result-item">
                                        <div className={iconClasses}>
                                            {React.createElement(icons[index % icons.length])}
                                        </div>
                                        <p className="text-slate-200 flex-1">{match}</p>
                                    </div>
                                );
                            })}
                        </div>
                    </div>
                );
            };

            ReactDOM.render(<Quiz />, document.getElementById('quiz-root'));
        </script>
    </body>
    </html>
    """
    
    # Hauteur dynamique selon le contenu
    components.html(quiz_html, height=493, width=None, scrolling=False)