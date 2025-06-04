import { useNavigate } from "react-router-dom";
import { socialLogin } from "../services/api";

interface Props {
  provider: string;
  label: string;
}

export default function SocialLoginButton({ provider, label }: Props) {
  const navigate = useNavigate();

  async function handleClick() {
    // Simulate provider sign-in then call the mocked API
    const token = await socialLogin(provider, "dummy_token");
    if (token) {
      localStorage.setItem("token", token);
      navigate("/dashboard");
    }
  }

  return (
    <button type="button" onClick={handleClick} style={{ margin: "0 0.5rem" }}>
      Login with {label}
    </button>
  );
}
