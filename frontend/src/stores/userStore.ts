import { defineStore } from "pinia";
import axios from "axios";

interface User {
  isAuthenticated: boolean;
  id: number | null;
  email: string | null;
  name: string | null;
  is_staff: boolean;
  access: string | null;
  refresh: string | null;
}

interface State {
  user: User;
  loading: boolean;
  error: string | null;
  refreshTimerId: number | null;
}

export const useUserStore = defineStore("user",{
  state: (): State => ({
    user: {
      isAuthenticated: false,
      id: null,
      email: null,
      name: null,
      is_staff: false,
      access: null,
      refresh: null,
    },
    loading: false,
    error: null,
    refreshTimerId: null,
  }),
  actions: {
    async initStore(): Promise<void> {
      const access = localStorage.getItem("user.access");
      const refresh = localStorage.getItem("user.refresh");

      if (access && refresh) {
        this.user.access = access;
        this.user.refresh = refresh;
        this.user.isAuthenticated = true;
        axios.defaults.headers.common["Authorization"] = `Bearer ${access}`;

        try {
          const response = await axios.get("/api/auth/me/", {
            headers: {
              Authorization: `Bearer ${access}`,
            },
          });
          this.setUserInfo(response.data);

          if (!this.refreshTimerId) {
            this.setupTokenRefresh();
          }
        } catch (error) {
          await this.refreshToken();
        }
      }
    },

    setupTokenRefresh(): void {
      if (this.refreshTimerId !== null) {
        clearTimeout(this.refreshTimerId);
        this.refreshTimerId = null;
      }

      if (this.user.access) {
        try {
          const payload = JSON.parse(atob(this.user.access.split('.')[1]));
          const expiryTime = payload.exp * 1000;
          const currentTime = Date.now();
          const timeUntilExpiry = expiryTime - currentTime;

          if (timeUntilExpiry > 0 && timeUntilExpiry < 24 * 60 * 60 * 1000) {
            const timeToRefresh = Math.max(timeUntilExpiry - 10 * 60 * 1000, 1000);

            this.refreshTimerId = window.setTimeout(() => {
              this.refreshToken();
            }, timeToRefresh);
          }
        } catch (error) {
          console.error("Błąd przy dekodowaniu tokena:", error);
        }
      }
    },

    setToken(data: { access: string; refresh: string }): void {
      this.user.access = data.access;
      this.user.refresh = data.refresh;
      this.user.isAuthenticated = true;
      localStorage.setItem("user.access", data.access);
      localStorage.setItem("user.refresh", data.refresh);
      axios.defaults.headers.common["Authorization"] = `Bearer ${data.access}`;

      this.setupTokenRefresh();
    },

    removeToken(): void {
      if (this.refreshTimerId !== null) {
        clearTimeout(this.refreshTimerId);
        this.refreshTimerId = null;
      }

      this.user.isAuthenticated = false;
      this.user.access = null;
      this.user.refresh = null;
      this.user.id = null;
      this.user.email = null;
      this.user.name = null;
      this.user.is_staff = false;
      localStorage.removeItem("user.access");
      localStorage.removeItem("user.refresh");
      localStorage.removeItem("user.id");
      localStorage.removeItem("user.email");
      localStorage.removeItem("user.name");
      localStorage.removeItem("user.is_staff");
      axios.defaults.headers.common["Authorization"] = "";
    },

    setUserInfo(user: Omit<User, 'isAuthenticated' | 'access' | 'refresh'>): void {
      this.user.id = user.id;
      this.user.email = user.email;
      this.user.name = user.name;
      this.user.is_staff = user.is_staff;
      localStorage.setItem("user.id", user.id?.toString() || "");
      localStorage.setItem("user.email", user.email || "");
      localStorage.setItem("user.name", user.name || "");
      localStorage.setItem("user.is_staff", user.is_staff.toString());
    },

    async refreshToken(): Promise<boolean> {
      if (!this.user.refresh) {
        this.removeToken();
        return false;
      }

      try {
        const response = await axios.post("/api/auth/refresh/", {
          refresh: this.user.refresh,
        });

        this.user.access = response.data.access;
        localStorage.setItem("user.access", response.data.access);
        axios.defaults.headers.common["Authorization"] = `Bearer ${response.data.access}`;
        console.log("Token odświeżony pomyślnie");

        this.setupTokenRefresh();
        return true;
      } catch (error) {
        console.error("Błąd odświeżania tokena:", error);
      }
    },

    logout(): void {
      this.removeToken();
    },
  },
});