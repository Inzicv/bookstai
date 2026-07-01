export function LoadingButton({
  loading,
  children,
  onClick,
}: {
  loading: boolean
  children: React.ReactNode
  onClick?: () => void | Promise<void>
}) {
  return (
    <button
      type={onClick ? 'button' : 'submit'}
      onClick={onClick}
      disabled={loading}
      className="inline-flex items-center justify-center rounded-full bg-violet-500 px-5 py-2.5 text-sm font-medium text-white shadow-lg shadow-violet-500/20 transition hover:bg-violet-400 focus:outline-none focus:ring-2 focus:ring-violet-300 focus:ring-offset-2 focus:ring-offset-slate-950 disabled:cursor-not-allowed disabled:opacity-60"
    >
      {loading ? 'Chargement...' : children}
    </button>
  )
}
