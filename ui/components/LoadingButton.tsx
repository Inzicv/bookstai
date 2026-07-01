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
      className="rounded-full bg-zinc-950 px-5 py-2.5 text-sm font-medium text-white disabled:cursor-not-allowed disabled:opacity-60"
    >
      {loading ? 'Chargement...' : children}
    </button>
  )
}

