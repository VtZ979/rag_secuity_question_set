import logo from '../assets/logo.svg'

export default function Header() {
    return (
        <header>
            <div className="logo">
            <img src={logo} alt="Security Knowledge Base Logo" />
            <h1>
                <span className="title-top">AUGMENTED SECURITY KNOWLEDGE BASE</span>
                {/* <span className="title-bottom"></span> */}
            </h1>
            </div>
        </header>
    )
}