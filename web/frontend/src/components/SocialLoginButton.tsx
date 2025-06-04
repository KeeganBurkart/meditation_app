import { useNavigate } from "react-router-dom";
import { socialLogin } from "../services/api";

interface Props {
  provider: string;
  label: string;
}

export default function SocialLoginButton({ provider, label }: Props) {
  const navigate = useNavigate();

  async function handleClick() {
    try {
      // TODO: Integrate real OAuth flows for each provider
      const providerToken = `${provider}_demo_token`;
      const token = await socialLogin(provider, providerToken);
      if (token) {
        localStorage.setItem("token", token);
        navigate("/dashboard");
      } else {
        alert("Social login failed");
      }
    } catch (err) {
      console.error(err);
      alert("Social login failed");
    }
  }

  return (
    <button type="button" onClick={handleClick} style={{ margin: "0 0.5rem" }}>
      Login with {label}
    </button>
  );
}
