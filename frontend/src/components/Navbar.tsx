import { Link, useNavigate, useLocation } from "react-router-dom";
import { useAuthStore } from "../store/authStore";

const links = [
  { to: "/profile", label: "Профіль" },
  { to: "/products", label: "Продукти" },
  { to: "/menu", label: "Меню" },
  { to: "/analytics", label: "Аналітика" },
];

export default function Navbar() {
  const { user, logout } = useAuthStore();
  const navigate = useNavigate();
  const location = useLocation();

  const handleLogout = () => {
    logout();
    navigate("/login");
  };

  return (
    <nav className="bg-primary shadow-md">
      <div className="max-w-6xl mx-auto px-4 flex items-center justify-between h-14">
        <Link to="/menu" className="text-white font-bold text-xl tracking-tight">
          SuperSportyk
        </Link>
        <div className="flex items-center gap-4">
          {links.map((l) => (
            <Link
              key={l.to}
              to={l.to}
              className={`text-sm font-medium px-2 py-1 rounded transition ${
                location.pathname === l.to
                  ? "bg-white text-primary"
                  : "text-white hover:bg-green-700"
              }`}
            >
              {l.label}
            </Link>
          ))}
          {user && (
            <span className="text-white text-sm ml-2">
              {user.username}
            </span>
          )}
          <button
            onClick={handleLogout}
            className="text-white border border-white text-sm px-3 py-1 rounded hover:bg-green-700 transition"
          >
            Вийти
          </button>
        </div>
      </div>
    </nav>
  );
}
