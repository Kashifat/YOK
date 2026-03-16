"use client"

import { createContext, useCallback, useContext, useEffect, useMemo, useState } from "react"

const AUTH_API_BASE = process.env.NEXT_PUBLIC_AUTH_API_URL ?? "http://localhost:8001/auth"
const ACCESS_TOKEN_KEY = "yok_access_token"
const REFRESH_TOKEN_KEY = "yok_refresh_token"
const USER_KEY = "yok_user"
const POST_AUTH_REDIRECT_KEY = "yok_post_auth_redirect"

export type AuthUser = {
  id: string
  role?: string
  email?: string
  name?: string
}

type LoginPayload = {
  courriel: string
  mot_de_passe: string
}

type RegisterPayload = {
  nom_complet: string
  courriel: string
  mot_de_passe: string
  telephone?: string
}

type AuthContextValue = {
  isAuthenticated: boolean
  isLoading: boolean
  user: AuthUser | null
  loginWithEmail: (payload: LoginPayload) => Promise<void>
  registerWithEmail: (payload: RegisterPayload) => Promise<void>
  logout: () => void
  startGoogleLogin: () => void
  startFacebookLogin: () => void
  requireAuth: (reason?: string) => boolean
}

const AuthContext = createContext<AuthContextValue | undefined>(undefined)

function decodeJwtPayload(token: string): Record<string, unknown> | null {
  try {
    const payload = token.split(".")[1]
    if (!payload) return null

    const normalized = payload.replace(/-/g, "+").replace(/_/g, "/")
    const padded = normalized.padEnd(Math.ceil(normalized.length / 4) * 4, "=")
    const decoded = atob(padded)
    return JSON.parse(decoded) as Record<string, unknown>
  } catch {
    return null
  }
}

function buildUserFromToken(token: string, fallback?: Partial<AuthUser>): AuthUser {
  const payload = decodeJwtPayload(token)
  const id = String(payload?.sub ?? fallback?.id ?? "")
  const role = typeof payload?.role === "string" ? payload.role : fallback?.role

  return {
    id,
    role,
    email: fallback?.email,
    name: fallback?.name,
  }
}

async function postJson<T>(url: string, data: Record<string, unknown>): Promise<T> {
  const response = await fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  })

  const body = await response.json().catch(() => null)
  if (!response.ok) {
    const message = (body && typeof body.detail === "string" && body.detail) || "Une erreur est survenue."
    throw new Error(message)
  }

  return body as T
}

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [isLoading, setIsLoading] = useState(true)
  const [accessToken, setAccessToken] = useState<string | null>(null)
  const [refreshToken, setRefreshToken] = useState<string | null>(null)
  const [user, setUser] = useState<AuthUser | null>(null)

  const persistSession = useCallback((nextAccessToken: string, nextRefreshToken: string, fallbackUser?: Partial<AuthUser>) => {
    const nextUser = buildUserFromToken(nextAccessToken, fallbackUser)

    localStorage.setItem(ACCESS_TOKEN_KEY, nextAccessToken)
    localStorage.setItem(REFRESH_TOKEN_KEY, nextRefreshToken)
    localStorage.setItem(USER_KEY, JSON.stringify(nextUser))

    setAccessToken(nextAccessToken)
    setRefreshToken(nextRefreshToken)
    setUser(nextUser)
  }, [])

  const clearSession = useCallback(() => {
    localStorage.removeItem(ACCESS_TOKEN_KEY)
    localStorage.removeItem(REFRESH_TOKEN_KEY)
    localStorage.removeItem(USER_KEY)

    setAccessToken(null)
    setRefreshToken(null)
    setUser(null)
  }, [])

  useEffect(() => {
    const params = new URLSearchParams(window.location.search)
    const accessFromUrl = params.get("access_token")
    const refreshFromUrl = params.get("refresh_token")

    if (accessFromUrl && refreshFromUrl) {
      persistSession(accessFromUrl, refreshFromUrl)

      params.delete("access_token")
      params.delete("refresh_token")
      const nextQuery = params.toString()
      const nextUrl = `${window.location.pathname}${nextQuery ? `?${nextQuery}` : ""}`
      window.history.replaceState({}, "", nextUrl)

      const redirectPath = sessionStorage.getItem(POST_AUTH_REDIRECT_KEY)
      if (redirectPath) {
        sessionStorage.removeItem(POST_AUTH_REDIRECT_KEY)
        window.location.replace(redirectPath)
        return
      }
    } else {
      const savedAccessToken = localStorage.getItem(ACCESS_TOKEN_KEY)
      const savedRefreshToken = localStorage.getItem(REFRESH_TOKEN_KEY)
      const savedUser = localStorage.getItem(USER_KEY)

      if (savedAccessToken && savedRefreshToken) {
        setAccessToken(savedAccessToken)
        setRefreshToken(savedRefreshToken)

        if (savedUser) {
          try {
            setUser(JSON.parse(savedUser) as AuthUser)
          } catch {
            setUser(buildUserFromToken(savedAccessToken))
          }
        } else {
          setUser(buildUserFromToken(savedAccessToken))
        }
      }
    }

    setIsLoading(false)
  }, [persistSession])

  const loginWithEmail = useCallback(async (payload: LoginPayload) => {
    type TokenPair = { access_token: string; refresh_token: string }
    const tokens = await postJson<TokenPair>(`${AUTH_API_BASE}/connexion`, payload)

    persistSession(tokens.access_token, tokens.refresh_token, { email: payload.courriel })
  }, [persistSession])

  const registerWithEmail = useCallback(async (payload: RegisterPayload) => {
    await postJson(`${AUTH_API_BASE}/inscription`, payload)
    await loginWithEmail({ courriel: payload.courriel, mot_de_passe: payload.mot_de_passe })
  }, [loginWithEmail])

  const logout = useCallback(() => {
    if (accessToken) {
      fetch(`${AUTH_API_BASE}/deconnecter`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ token: accessToken }),
      }).catch(() => undefined)
    }

    clearSession()
  }, [accessToken, clearSession])

  const startSocialLogin = useCallback((provider: "google" | "facebook") => {
    const pathWithQuery = `${window.location.pathname}${window.location.search}`
    sessionStorage.setItem(POST_AUTH_REDIRECT_KEY, pathWithQuery)
    window.location.href = `${AUTH_API_BASE}/oauth/${provider}`
  }, [])

  const requireAuth = useCallback((reason?: string) => {
    if (accessToken && user?.id) return true

    const pathWithQuery = `${window.location.pathname}${window.location.search}`
    sessionStorage.setItem(POST_AUTH_REDIRECT_KEY, pathWithQuery)

    const params = new URLSearchParams()
    if (reason) {
      params.set("reason", reason)
    }

    const query = params.toString()
    window.location.href = `/compte${query ? `?${query}` : ""}`
    return false
  }, [accessToken, user?.id])

  const value = useMemo<AuthContextValue>(() => ({
    isAuthenticated: Boolean(accessToken && user?.id),
    isLoading,
    user,
    loginWithEmail,
    registerWithEmail,
    logout,
    startGoogleLogin: () => startSocialLogin("google"),
    startFacebookLogin: () => startSocialLogin("facebook"),
    requireAuth,
  }), [accessToken, isLoading, loginWithEmail, registerWithEmail, logout, requireAuth, startSocialLogin, user])

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}

export function useAuth() {
  const context = useContext(AuthContext)
  if (!context) {
    throw new Error("useAuth must be used within an AuthProvider")
  }
  return context
}
